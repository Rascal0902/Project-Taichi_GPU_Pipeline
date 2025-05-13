from light_module.ImageManager import ImageManager
from light_module.Meshloader import MeshLoader
from light_module.SpaceChanger import SpaceChanger

from light_module.shader.ENV_LIGHT_Shader import Environment_Light_Shader
from light_module.shader.ENV_NOLIGHT_Shader import Environment_Shader
from light_module.shader.HUMAN_Shader import SMPL_Shader
from light_module.shader.NORMAL_LIGHT_Shader import Light_Shader
from light_module.shader.NORMAL_NOLIGHT_Shader import NoLight_Shader
from light_module.shader.PLY_Shader import PLY_Shader

from light_module.LightComponent import LightComponent


class ShaderManager:
    def __init__(self, mesh: MeshLoader, space: SpaceChanger, img: ImageManager, env: ImageManager, N=1, BACKFACE=True):
        self.mesh = mesh
        self.space = space
        self.img = img
        self.env = env
        self.N = N
        self.BACKFACE = BACKFACE

        self.shaderID = None
        self.shaderMODE = None
        self.shader = None

        self.allocate = True

    def setShader(self, ID, MODE):
        self.shaderID = ID
        self.shaderMODE = MODE

    def render(self, space, cam_posx, cam_posy, cam_posz):
        if self.shaderMODE == "ENV_LIGHT" and LightComponent.rendered_len != 0:
            if self.allocate:
                self.shader = Environment_Light_Shader(self.mesh, self.space, self.img, self.env, self.N, self.BACKFACE)
                self.allocate = False

            self.shader.vertexShader(space.object_to_world_Matrix,
                                        space.world_to_view_Matrix,
                                        space.view_to_clip_Matrix)

            self.shader.rasterizer(cam_posx, cam_posy, cam_posz)
            return

        if self.shaderMODE == "ENV_NOLIGHT" or (self.shaderMODE == "ENV_LIGHT" and LightComponent.rendered_len == 0):
            if self.allocate:
                self.shader = Environment_Shader(self.mesh, self.space, self.img, self.env, self.N, self.BACKFACE)
                self.allocate = False

            self.shader.vertexShader(space.object_to_world_Matrix,
                                        space.world_to_view_Matrix,
                                        space.view_to_clip_Matrix)

            self.shader.rasterizer(cam_posx, cam_posy, cam_posz)
            return

        if self.shaderMODE == "HUMAN" and LightComponent.rendered_len != 0:
            if self.allocate:
                self.shader = SMPL_Shader(self.mesh, self.space, self.img, self.BACKFACE)
                self.allocate = False

            self.shader.vertexShader(space.object_to_world_Matrix,
                                      space.world_to_view_Matrix,
                                      space.view_to_clip_Matrix)

            self.shader.rasterizer(cam_posx, cam_posy, cam_posz)
            return

        elif self.shaderMODE == "NORMAL_LIGHT" and LightComponent.rendered_len != 0:
            if self.allocate:
                self.shader = Light_Shader(self.mesh, self.space, self.img, self.BACKFACE)
                self.allocate = False

            self.shader.vertexShader(space.object_to_world_Matrix,
                                      space.world_to_view_Matrix,
                                      space.view_to_clip_Matrix)

            self.shader.rasterizer(cam_posx, cam_posy, cam_posz)
            return

        elif self.shaderMODE == "PLY_ENV" and LightComponent.rendered_len != 0:
            if self.allocate:
                self.shader = PLY_Shader(self.mesh, self.space, self.img, self.BACKFACE)
                self.allocate = False

            self.shader.vertexShader(space.object_to_world_Matrix,
                                     space.world_to_view_Matrix,
                                     space.view_to_clip_Matrix)

            self.shader.rasterizer(cam_posx, cam_posy, cam_posz)



        else:  # "NORMAL_NOLIGHT" or No Lights
            if self.allocate:
                self.shader = NoLight_Shader(self.mesh, self.space, self.img, self.BACKFACE)
                self.allocate = False

            self.shader.vertexShader(space.object_to_world_Matrix,
                                      space.world_to_view_Matrix,
                                      space.view_to_clip_Matrix)

            self.shader.rasterizer(cam_posx, cam_posy, cam_posz)
            return

