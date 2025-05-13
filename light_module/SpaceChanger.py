import torch
import numpy as np
import taichi as ti

class SpaceChanger:
    def __init__(self, id, w, h, device=None, pointdtype=None):
        self.w, self.h = w, h
        self.aspect = self.w / self.h

        self.object_to_world_Matrix = None
        self.world_to_view_Matrix = None
        self.view_to_clip_Matrix = None
        self.ndc_to_screen = torch.tensor([[self.w * 0.5, 0.0, 0.0, 0.0],
                                                [0.0, self.h * 0.5, 0.0, 0.0],
                                                [0.0, 0.0, 0.5, 0.0],
                                                [self.w * 0.5, self.h * 0.5, 0.5, 1.0]]
                                                , device=device, dtype=pointdtype).T

        self.device, self.pointdtype = device, pointdtype
        print(f"id: {id}, obj.points : device -> {device}, dtype -> {pointdtype}")
        # print("initialized SpaceChanger")

    def set_object_to_world_space_torch(self, scale, translation, rotation, is_radian=True):

        temp = torch.eye(3, dtype=self.pointdtype, device=self.device) * scale

        translation = torch.tensor(translation, device=self.device, dtype=self.pointdtype)

        if rotation != (0.0, 0.0, 0.0):
            rotation = torch.tensor(rotation, device=self.device, dtype=self.pointdtype)
            rot_theta = torch.linalg.vector_norm(rotation, ord=2, dtype=self.pointdtype)

            u = rotation / rot_theta  # normalization
            if not is_radian:
                rot_theta *= (np.pi / 180.0)

            k = torch.tensor([[0.0, -u[2], u[1]], [u[2], 0.0, -u[0]], [-u[1], u[0], 0.0]]
                             , dtype=self.pointdtype, device=self.device)

            rodrigues = torch.eye(3, dtype=self.pointdtype, device=self.device) + \
                        (1.0 - torch.math.cos(rot_theta)) * (k @ k) + \
                        torch.math.sin(rot_theta) * k

        else:
            rodrigues = torch.eye(3, dtype=self.pointdtype, device=self.device)

        temp = rodrigues @ temp

        result4X4 = torch.zeros((4, 4), dtype=self.pointdtype, device=self.device)
        result4X4[:3, :3] = temp
        result4X4[3, 3] = 1.0

        for i in range(0, 3):
            result4X4[i, 3] = translation[i]

        self.object_to_world_Matrix = result4X4

    def set_world_to_2Dscreen_torch(self, camera: ti.ui.Camera):
        self.world_to_view_Matrix = torch.tensor(camera.get_view_matrix().T
                                                 , device=self.device, dtype=self.pointdtype)

        self.view_to_clip_Matrix = torch.tensor(camera.get_projection_matrix(self.aspect).T
                                                , device=self.device, dtype=self.pointdtype)




