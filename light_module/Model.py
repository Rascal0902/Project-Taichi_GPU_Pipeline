import taichi as ti
import torch
import os

from light_module.ImageManager import ImageManager
from light_module.Meshloader import MeshLoader
from light_module.SpaceChanger import SpaceChanger
from light_module.ShaderManager import ShaderManager

from light_module.shader.Storage import Storage, z_buffering
from light_module.Meshloader import normal_generator


# using camera -> 1) Model.Storage.setCamera -> to get view direction
#                 2) Model.camera -> to get one camera
#                 3) Model -> set world to view Matrix

def Modelrender(canvas: ti.ui.Canvas, camera: ti.ui.Camera, cam_pos, MODE=None):
    if MODE is None:

        # Model.Storage.setCamera(camera)
        # Model.Storage.initialize_buffer_array()
        Model.Storage.initialize_window()

        Model.camera = camera

        for key, value in Model.model.items():
            if value["mesh"].render:
                value["spaceChanger"].set_world_to_2Dscreen_torch(camera)
                value["shader"].render(value["spaceChanger"], *cam_pos)  # camera for getting view direction

        # z_buffering()
        pixel = Model.Storage.get_pixel()
        canvas.set_image(pixel)


class Model:
    model = {}
    env_map = None

    def __init__(self, camera: ti.ui.Camera, screensize):
        Model.camera = camera
        self.w, self.h = screensize
        Model.Storage = Storage(self.w, self.h)

    def initialize_env_map(self, current_dir, filename, Diffusion=False):
        Model.env_map = ImageManager()
        if not Diffusion:
            env_mapPath = os.path.join(current_dir, 'light_module', 'env_map', filename)
        else:
            env_mapPath = os.path.join(current_dir, 'light_module', 'diffusion', 'outputs', 'envmap', filename)
        Model.env_map.loadImage(env_mapPath)

    def addModel(self, id):
        Model.model[id] = {}

    def setTexture(self, id, image_path):
        Model.model[id]["texture"] = ImageManager()
        Model.model[id]["texture"].loadImage(image_path)

    def setMesh(self, id, mesh_path, render=True, ply=False):
        if ply == False:
            Model.model[id]["mesh"] = MeshLoader(mesh_path)
            Model.model[id]["mesh"].obj_load()
            Model.model[id]["mesh"].obj_render(render)

        if ply == True:
            Model.model[id]["mesh"] = MeshLoader(mesh_path)
            Model.model[id]["mesh"].ply_load()
            Model.model[id]["mesh"].ply_render(render)

    def setSpaceChanger(self, id, transform_settings: tuple):
        sampledata = Model.model[id]["mesh"].obj["vertices"]
        sampledevice = sampledata.device
        sampledtype = sampledata.dtype
        Model.model[id]["spaceChanger"] = SpaceChanger(id, self.w, self.h, sampledevice, sampledtype)

        Model.model[id]["spaceChanger"].set_object_to_world_space_torch(*transform_settings, is_radian=False)
        Model.model[id]["spaceChanger"].set_world_to_2Dscreen_torch(Model.camera)

    def setShader(self, id, MODE, N=1, BACKFACE=True):
        Model.model[id]["shader"] = ShaderManager(Model.model[id]["mesh"], Model.model[id]["spaceChanger"],
                                                  Model.model[id]["texture"], Model.env_map, N=N, BACKFACE=BACKFACE)
        Model.model[id]["shader"].setShader(id, MODE)

    def updatespace(self, id, transform_settings: tuple):
        Model.model[id]["spaceChanger"].set_object_to_world_space_torch(*transform_settings, is_radian=False)

    def updateMeshHard(self, id, mesh_path, vertices, normals, MODE='LIGHT'):
        if MODE == 'LIGHT':
            temp = MeshLoader(mesh_path)
            temp.obj_load()
            Model.model[id]["mesh"].obj["vertices"] = temp.obj["vertices"]
            Model.model[id]["mesh"].obj["normals"] = temp.obj["normals"]

        if MODE == 'VTON':
            if vertices is None and normals is None:
                return

            if isinstance(vertices, ti.MatrixField):
                vertices_np = vertices.to_numpy()
                vertices = torch.from_numpy(vertices_np).float().to('cuda:0')

            if vertices is not None:
                Model.model[id]["mesh"].obj["vertices"] = vertices
            if normals is not None:
                Model.model[id]["mesh"].obj["normals"] = normals
            else:
                Model.model[id]["mesh"].verts.from_torch(vertices)
                Model.model[id]["mesh"].obj_faces.from_torch(Model.model[id]["mesh"].obj["faces"])
                normal_generator(vertices=Model.model[id]["mesh"].verts, faces=Model.model[id]["mesh"].obj_faces
                                 , normals=Model.model[id]["mesh"].normals)
