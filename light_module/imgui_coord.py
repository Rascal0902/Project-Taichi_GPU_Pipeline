import taichi as ti
import numpy as np
import torch

from light_module.SpaceChanger import SpaceChanger


class Util:
    def renderingtestSetup(self, camera, width, height):
        temp = SpaceChanger("point", width, height, device='cuda', pointdtype=torch.float32)
        applyTransform_settings = (1.0, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        temp.set_object_to_world_space_torch(*applyTransform_settings, is_radian=False)
        temp.set_world_to_2Dscreen_torch(camera)
        return temp

    def getPoint(self, posx, posy, posz, temp):
        item = np.array([posx, posy, posz, 1.0], dtype=np.float32)
        item_tensor = torch.from_numpy(item).to('cuda')

        obj_column_tensor = item_tensor.T  # object space 4D column vector
        world_column_tensor = temp.object_to_world_Matrix @ obj_column_tensor  # world space 4D column vector
        view_column_tensor = temp.world_to_view_Matrix @ world_column_tensor  # view space 4D column vector
        clip_column_tensor = temp.view_to_clip_Matrix @ view_column_tensor  # clip space 4D vector (ndc)

        norm = clip_column_tensor[3]
        clip_column_tensor = clip_column_tensor.clone()
        clip_column_tensor /= norm

        screen_column_tensor = temp.ndc_to_screen @ clip_column_tensor  # screen space 4D vector

        point2d = screen_column_tensor.T

        return point2d

    def displayPoint(self, posx, posy, posz, temp, width, height, canvas, field, camera: ti.ui.Camera):
        temp.set_world_to_2Dscreen_torch(camera)
        point2d = self.getPoint(posx, posy, posz, temp).cpu()
        field[0] = np.array([point2d[0] / width, point2d[1] / height])
        radius = 0.005
        canvas.circles(field, radius, (1.0, 0.0, 1.0))

    def displayCoordinate(self, temp, width, height, canvas: ti.ui.Canvas, field, edge, camera: ti.ui.Camera):
        temp.set_world_to_2Dscreen_torch(camera)
        point2d0 = self.getPoint(0.0, 0.0, 0.0, temp).cpu()
        point2dx = self.getPoint(3.0, 0.0, 0.0, temp).cpu()
        point2dy = self.getPoint(0.0, 3.0, 0.0, temp).cpu()
        point2dz = self.getPoint(0.0, 0.0, 3.0, temp).cpu()

        strength = 0.003
        edge[0] = np.array([0, 1])
        field[0] = np.array([point2d0[0] / width, point2d0[1] / height])

        field[1] = np.array([point2dx[0] / width, point2dx[1] / height])
        canvas.lines(field, strength, edge, (1.0, 0.0, 0.0))

        field[1] = np.array([point2dy[0] / width, point2dy[1] / height])
        canvas.lines(field, strength, edge, (0.0, 1.0, 0.0))

        field[1] = np.array([point2dz[0] / width, point2dz[1] / height])
        canvas.lines(field, strength, edge, (0.0, 0.0, 1.0))
