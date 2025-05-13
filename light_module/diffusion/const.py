dataset = "./light_module/diffusion/inputs"

ball_size = 256
ball_dilate = 20

prompt = "a perfect mirrored reflective chrome ball sphere"
prompt_dark = "a perfect black dark mirrored reflective chrome ball sphere"
negative_prompt = "matte, diffuse, flat, dull"
model_option = "sdxl_fast"

output_dir = "./light_module/diffusion/outputs"
img_height = 512
img_width = 512

seed = "auto"
denoising_step = 30
control_scale = 0.5
guidance_scale = 5.0

no_controlnet = use_controlnet = True
no_force_square = force_square = True
no_random_loader = random_loader = True

is_cpu = cpu = False
offload = False
limit_input = 0

no_lora = use_lora = True

lora_path = "light_module/diffusion/models/ThisIsTheFinal-lora-hdr-continuous-largeT@900/0_-5/checkpoint-2500"
lora_scale = 0.75

no_torch_compile = use_torch_compile = True

algorithm = "normal"

agg_mode = "median"
strength = 0.8
num_iteration = 2
ball_per_iteration = 30
no_save_intermediate = save_intermediate = True
cache_dir = "./light_module/diffusion/temp_inpaint_iterative"

idx = 0
total = 1
max_negative_ev = -5
ev = "0"

ball_dir = "./light_module/diffusion/outputs/square"
envmap_dir = "./light_module/diffusion/outputs/envmap"
envmap_height = 512
scale = 4
threads = 8
