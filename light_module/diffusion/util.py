import skimage
try:
    import ezexr
except:
    pass

import numpy as np
import torch
import os

from light_module.diffusion.const import *

def get_ball_location(image_data):
    if 'boundary' in image_data:
        x = image_data["boundary"]["x"]
        y = image_data["boundary"]["y"]
        r = image_data["boundary"]["size"]

        half_dilate = ball_dilate // 2

        if x - half_dilate < 0: x += half_dilate
        if y - half_dilate < 0: y += half_dilate

        if x + r + half_dilate > img_width: x -= half_dilate
        if y + r + half_dilate > img_height: y -= half_dilate

    else:
        x, y, r = (
        (img_width // 2) - (ball_size // 2), (img_height // 2) - (ball_size // 2), ball_size)
    return x, y, r


def interpolate_embedding(pipe):
    print("interpolate embedding...")

    ev_list = [float(x) for x in ev.split(",")]
    interpolants = [ev / max_negative_ev for ev in ev_list]

    print("EV : ", ev_list)
    print("EV : ", interpolants)

    prompt_normal = prompt
    _prompt_dark = prompt_dark
    prompt_embeds_normal, _, pooled_prompt_embeds_normal, _ = pipe.pipeline.encode_prompt(prompt_normal)
    prompt_embeds_dark, _, pooled_prompt_embeds_dark, _ = pipe.pipeline.encode_prompt(_prompt_dark)

    interpolate_embeds = []
    for t in interpolants:
        int_prompt_embeds = prompt_embeds_normal + t * (prompt_embeds_dark - prompt_embeds_normal)
        int_pooled_prompt_embeds = pooled_prompt_embeds_normal + t * (
                    pooled_prompt_embeds_dark - pooled_prompt_embeds_normal)

        interpolate_embeds.append((int_prompt_embeds, int_pooled_prompt_embeds))

    return dict(zip(ev_list, interpolate_embeds))


def create_envmap_grid(size: int):
    """
    BLENDER CONVENSION
    Create the grid of environment map that contain the position in sperical coordinate
    Top left is (0,0) and bottom right is (pi/2, 2pi)
    """

    theta = torch.linspace(0, np.pi * 2, size * 2)
    phi = torch.linspace(0, np.pi, size)

    theta, phi = torch.meshgrid(theta, phi, indexing='xy')

    theta_phi = torch.cat([theta[..., None], phi[..., None]], dim=-1)
    theta_phi = theta_phi.numpy()
    return theta_phi


def get_normal_vector(incoming_vector: np.ndarray, reflect_vector: np.ndarray):
    """
    BLENDER CONVENSION
    incoming_vector: the vector from the point to the camera
    reflect_vector: the vector from the point to the light source
    """
    # N = 2(R ⋅ I)R - I
    N = (incoming_vector + reflect_vector) / np.linalg.norm(incoming_vector + reflect_vector, axis=-1, keepdims=True)
    return N


def get_cartesian_from_spherical(theta: np.array, phi: np.array, r=1.0):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.concatenate([x[..., None], y[..., None], z[..., None]], axis=-1)


def process_image(file_name: str):
    I = np.array([1, 0, 0])

    envmap_output_path = os.path.join(envmap_dir, file_name)
    if os.path.exists(envmap_output_path):
        print("Skipped.")
        return None

    ball_path = os.path.join(ball_dir, file_name)
    if file_name.endswith(".exr"):
        ball_image = ezexr.imread(ball_path)
    else:
        try:
            ball_image = skimage.io.imread(ball_path)
            ball_image = skimage.img_as_float(ball_image)
        except:
            return None

    env_grid = create_envmap_grid(envmap_height * scale)
    reflect_vec = get_cartesian_from_spherical(env_grid[..., 1], env_grid[..., 0])
    normal = get_normal_vector(I[None, None], reflect_vec)

    pos = (normal + 1.0) / 2
    pos = 1.0 - pos
    pos = pos[..., 1:]

    env_map = None

    with torch.no_grad():
        grid = torch.from_numpy(pos)[None].float()
        grid = grid * 2 - 1

        ball_image = torch.from_numpy(ball_image[None]).float()
        ball_image = ball_image.permute(0, 3, 1, 2)  # [1,3,H,W]

        env_map = torch.nn.functional.grid_sample(ball_image, grid, mode='bilinear', padding_mode='border',
                                                  align_corners=True)
        env_map = env_map[0].permute(1, 2, 0).numpy()

    env_map_default = skimage.transform.resize(env_map, (envmap_height, envmap_height * 2),
                                               anti_aliasing=True)
    if file_name.endswith(".exr"):
        ezexr.imwrite(envmap_output_path, env_map_default.astype(np.float32))
    else:
        env_map_default = skimage.img_as_ubyte(env_map_default)
        skimage.io.imsave(envmap_output_path, env_map_default)
    return None