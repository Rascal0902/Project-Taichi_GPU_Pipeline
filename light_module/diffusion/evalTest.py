import torch
import time
import os
from tqdm.auto import tqdm

from light_module.diffusion.relighting.inpainter import BallInpainter

from light_module.diffusion.relighting.mask_utils import MaskGenerator
from light_module.diffusion.relighting.ball_processor import get_ideal_normal_ball
from light_module.diffusion.relighting.dataset import GeneralLoader
from light_module.diffusion.relighting.utils import name2hash
import light_module.diffusion.relighting.dist_utils as dist_util

from light_module.diffusion.relighting.argument import (
    SD_MODELS,
    CONTROLNET_MODELS
)

from light_module.diffusion.const import *
from light_module.diffusion.util import interpolate_embedding, get_ball_location, process_image


def diffusion(img_width = img_width, img_height = img_height, seed = seed, guidance_scale = guidance_scale):
    torch.cuda.empty_cache()

    start = time.time()

    if is_cpu:
        device = torch.device("cpu")
        torch_dtype = torch.float32
    else:
        device = dist_util.dev()
        torch_dtype = torch.float16

    print(f"is_cpu:{is_cpu}")
    assert ball_dilate % 2 == 0  # ball dilation should be symmetric

    if model_option in ["sdxl", "sdxl_fast", "sdxl_turbo"] and use_controlnet:
        model, controlnet = SD_MODELS[model_option], CONTROLNET_MODELS[model_option]
        pipe = BallInpainter.from_sdxl(
            model=model,
            controlnet=controlnet,
            device=device,
            torch_dtype=torch_dtype,
            offload=offload
        )
    elif model_option in ["sdxl", "sdxl_fast", "sdxl_turbo"] and not use_controlnet:
        model = SD_MODELS[model_option]
        pipe = BallInpainter.from_sdxl(
            model=model,
            controlnet=None,
            device=device,
            torch_dtype=torch_dtype,
            offload=offload
        )
    elif use_controlnet:
        model, controlnet = SD_MODELS[model_option], CONTROLNET_MODELS[model_option]
        pipe = BallInpainter.from_sd(
            model=model,
            controlnet=controlnet,
            device=device,
            torch_dtype=torch_dtype,
            offload=offload
        )
    else:
        model = SD_MODELS[model_option]
        pipe = BallInpainter.from_sd(
            model=model,
            controlnet=None,
            device=device,
            torch_dtype=torch_dtype,
            offload=offload
        )

    if model_option in ["sdxl_turbo"]:
        # Guidance scale is not supported in sdxl_turbo
        guidance_scale = 0.0

    if lora_scale > 0 and lora_path is None:
        raise ValueError("lora scale is not 0 but lora path is not set")

    if (lora_path is not None) and (use_lora):
        print(f"using lora path {lora_path}")
        print(f"using lora scale {lora_scale}")
        pipe.pipeline.load_lora_weights(lora_path)
        pipe.pipeline.fuse_lora(lora_scale=lora_scale)  # fuse lora weight w' = w + \alpha \Delta w
        enabled_lora = True
    else:
        enabled_lora = False

    if use_torch_compile:
        try:
            print("compiling unet model")
            start_time = time.time()
            pipe.pipeline.unet = torch.compile(pipe.pipeline.unet, mode="reduce-overhead", fullgraph=True)
            print("Model compilation time: ", time.time() - start_time)
        except:
            pass

    # default height for sdxl is 1024, if not set, we set default height.
    if model_option == "sdxl" and img_height == 0 and img_width == 0:
        img_height = 1024
        img_width = 1024

    # load dataset
    Dataset = GeneralLoader(
        root=dataset,
        resolution=(img_width, img_height),
        force_square=force_square,
        return_dict=True,
        random_shuffle=random_loader,
        process_id=idx,
        process_total=total,
        limit_input=limit_input,
    )

    # interpolate embedding
    embedding_dict = interpolate_embedding(pipe)

    # prepare mask and normal ball
    mask_generator = MaskGenerator()
    normal_ball, mask_ball = get_ideal_normal_ball(size=ball_size + ball_dilate)
    _, mask_ball_for_crop = get_ideal_normal_ball(size=ball_size)

    # make output directory if not exist
    raw_output_dir = os.path.join(output_dir, "raw")
    control_output_dir = os.path.join(output_dir, "control")
    square_output_dir = os.path.join(output_dir, "square")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(raw_output_dir, exist_ok=True)
    os.makedirs(control_output_dir, exist_ok=True)
    os.makedirs(square_output_dir, exist_ok=True)

    # create split seed
    # please DO NOT manual replace this line, use --seed option instead
    seeds = seed.split(",")

    for image_data in tqdm(Dataset):
        input_image = image_data["image"]
        image_path = image_data["path"]

        for ev, (prompt_embeds, pooled_prompt_embeds) in embedding_dict.items():
            # create output file name (we always use png to prevent quality loss)
            ev_str = str(ev).replace(".", "") if ev != 0 else "-00"
            outname = os.path.basename(image_path).split(".")[0] + f"_ev{ev_str}"

            # we use top-left corner notation (which is different from aj.aek's center point notation)
            x, y, r = get_ball_location(image_data)

            # create inpaint mask
            mask = mask_generator.generate_single(
                input_image, mask_ball,
                x - ball_dilate // 2,
                y - ball_dilate // 2,
                r + ball_dilate
            )

            seeds = tqdm(seeds, desc="seeds") if len(seeds) > 10 else seeds

            # replacely create image with differnt seed
            for seed in seeds:
                start_time = time.time()
                # set seed, if seed auto we use file name as seed
                if seed == "auto":
                    filename = os.path.basename(image_path).split(".")[0]
                    seed = name2hash(filename)
                    outpng = f"{outname}.png"
                    cache_name = f"{outname}"
                else:
                    seed = int(seed)
                    outpng = f"{outname}_seed{seed}.png"
                    cache_name = f"{outname}_seed{seed}"
                # skip if file exist, useful for resuming
                if os.path.exists(os.path.join(square_output_dir, outpng)):
                    continue
                generator = torch.Generator().manual_seed(seed)
                kwargs = {
                    "prompt_embeds": prompt_embeds,
                    "pooled_prompt_embeds": pooled_prompt_embeds,
                    'negative_prompt': negative_prompt,
                    'num_inference_steps': denoising_step,
                    'generator': generator,
                    'image': input_image,
                    'mask_image': mask,
                    'strength': 1.0,
                    'current_seed': seed,  # we still need seed in the pipeline!
                    'controlnet_conditioning_scale': control_scale,
                    'height': img_height,
                    'width': img_width,
                    'normal_ball': normal_ball,
                    'mask_ball': mask_ball,
                    'x': x,
                    'y': y,
                    'r': r,
                    'guidance_scale': guidance_scale,
                }

                if enabled_lora:
                    kwargs["cross_attention_kwargs"] = {"scale": lora_scale}

                if algorithm == "normal":
                    output_image = pipe.inpaint(**kwargs).images[0]
                elif algorithm == "iterative":
                    # This is still buggy
                    print("using inpainting iterative, this is going to take a while...")
                    kwargs.update({
                        "strength": strength,
                        "num_iteration": num_iteration,
                        "ball_per_iteration": ball_per_iteration,
                        "agg_mode": agg_mode,
                        "save_intermediate": save_intermediate,
                        "cache_dir": os.path.join(cache_dir, cache_name),
                    })
                    output_image = pipe.inpaint_iterative(**kwargs)
                else:
                    raise NotImplementedError(f"Unknown algorithm {algorithm}")

                square_image = output_image.crop((x, y, x + r, y + r))

                # return the most recent control_image for sanity check
                control_image = pipe.get_cache_control_image()
                if control_image is not None:
                    control_image.save(os.path.join(control_output_dir, outpng))

                # save image
                output_image.save(os.path.join(raw_output_dir, outpng))
                square_image.save(os.path.join(square_output_dir, outpng))

                del output_image
                del square_image
                del control_image  # 추가: control_image 삭제
                torch.cuda.empty_cache()  # 추가: 캐시 비우기

    # make output directory if not exist
    os.makedirs(envmap_dir, exist_ok=True)

    # get all file in the directory
    files = sorted(os.listdir(ball_dir))

    for file in tqdm(files):
        process_image(file)

    end = time.time()

    print(f"time: {end - start}")


if __name__ == "__main__":
    diffusion()
