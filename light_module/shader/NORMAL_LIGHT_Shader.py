import torch
import taichi as ti

from light_module.LightComponent import LightComponent
from light_module.shader.Storage import Storage, tri_area, barycentric_coord, set_buffer

# from light_module.shader.Storage import buffer


@ti.data_oriented
class Light_Shader:
    def __init__(self, mesh, space, img, BACKFACE=True):
        self.ti_face = ti.field(dtype=ti.i32, shape=(mesh.obj['faces'].shape[0], 3, 3))
        self.ti_texcoord = ti.Vector.field(2, dtype=ti.f32, shape=(mesh.obj['texcoords'].shape[0]))

        self.world = ti.Vector.field(4, dtype=ti.f32, shape=mesh.obj['vertices'].shape[0])
        self.ndc = ti.Vector.field(4, dtype=ti.f32, shape=mesh.obj['vertices'].shape[0])
        self.normal = ti.Vector.field(3, dtype=ti.f32, shape=mesh.obj['normals'].shape[0])

        self.mesh = mesh
        self.img = img
        self.BACKFACE = BACKFACE

        temp = (space.ndc_to_screen.T).cpu().numpy()
        self.ti_ndc_to_screen = ti.Matrix([[temp[0][0], temp[0][1], temp[0][2], temp[0][3]],
                                           [temp[1][0], temp[1][1], temp[1][2], temp[1][3]],
                                           [temp[2][0], temp[2][1], temp[2][2], temp[2][3]],
                                           [temp[3][0], temp[3][1], temp[3][2], temp[3][3]]])

    def vertexShader(self, object_to_world_Matrix, world_to_view_Matrix, view_to_clip_Matrix):
        obj_column_tensor = torch.cat((self.mesh.obj['vertices'],
                                       torch.ones((self.mesh.obj['vertices'].shape[0], 1)
                                                  ).to('cuda')), dim=1).T  # object space 4D column vector

        world_column_tensor = object_to_world_Matrix @ obj_column_tensor  # world space 4D column vector
        self.world.from_torch(world_column_tensor.T)

        view_column_tensor = world_to_view_Matrix @ world_column_tensor  # view space 4D column vector
        clip_column_tensor = view_to_clip_Matrix @ view_column_tensor  # clip space 4D vector (ndc)
        norm = clip_column_tensor[3]
        clip_column_tensor = clip_column_tensor.clone()
        clip_column_tensor /= norm

        self.ndc.from_torch(clip_column_tensor.T)

        obj_normal_tensor = self.mesh.obj['normals'].T  # object space 3D normal vector
        normal_Matrix = torch.inverse(object_to_world_Matrix[:3, :3]).T
        self.normal.from_torch((normal_Matrix @ obj_normal_tensor).T)

        self.ti_face.from_torch(self.mesh.obj["faces"])
        self.ti_texcoord.from_torch(self.mesh.obj["texcoords"])

    @ti.kernel
    def rasterizer(self, cam_posx:ti.f32, cam_posy:ti.f32, cam_posz:ti.f32):
        for index in range(self.ti_face.shape[0]):

            # triangle ndc verts (row 4x1)
            v1 = self.ndc[int(self.ti_face[index, 0, 0])]
            v2 = self.ndc[int(self.ti_face[index, 1, 0])]
            v3 = self.ndc[int(self.ti_face[index, 2, 0])]

            screen_v1 = v1 @ self.ti_ndc_to_screen
            screen_v2 = v2 @ self.ti_ndc_to_screen
            screen_v3 = v3 @ self.ti_ndc_to_screen

            # make bounding box
            min_x = int(min(screen_v1[0], screen_v2[0], screen_v3[0]))
            max_x = int(max(screen_v1[0], screen_v2[0], screen_v3[0]))
            min_y = int(min(screen_v1[1], screen_v2[1], screen_v3[1]))
            max_y = int(max(screen_v1[1], screen_v2[1], screen_v3[1]))

            # clip bounding box
            min_x = max(min_x, 1)
            max_x = min(max_x, Storage.w - 1)
            min_y = max(min_y, 1)
            max_y = min(max_y, Storage.h - 1)

            v1_2d = ti.Vector([screen_v1[0], screen_v1[1]])
            v2_2d = ti.Vector([screen_v2[0], screen_v2[1]])
            v3_2d = ti.Vector([screen_v3[0], screen_v3[1]])

            # compute area with cross product
            area = tri_area(v1_2d, v2_2d, v3_2d)

            # backface culling
            if self.BACKFACE and area < 0.0:
                continue

            for x, y in ti.ndrange((min_x - 1, max_x + 1), (min_y - 1, max_y + 1)):
                key = ti.Vector([x + 0.5, y + 0.5])

                w = barycentric_coord(key, v1_2d, v2_2d, v3_2d)
                w0 = w[0]
                w1 = w[1]
                w2 = w[2]

                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    # compute depth
                    depth_pos = float(w0 * screen_v1[2] + w1 * screen_v2[2] + w2 * screen_v3[2])

                    # barycentric interpolation
                    fragment_pos = (w0 * self.world[int(self.ti_face[index, 0, 0])] + w1 * self.world[
                        int(self.ti_face[index, 1, 0])]
                                    + w2 * self.world[int(self.ti_face[index, 2, 0])])

                    # get texture color
                    tex_pos = (w0 * self.ti_texcoord[int(self.ti_face[index, 0, 1])] + w1 * self.ti_texcoord[
                        int(self.ti_face[index, 1, 1])]
                               + w2 * self.ti_texcoord[int(self.ti_face[index, 2, 1])])

                    normal = (w0 * self.normal[int(self.ti_face[index, 0, 2])] + w1 * self.normal[
                        int(self.ti_face[index, 1, 2])]
                              + w2 * self.normal[int(self.ti_face[index, 2, 2])])

                    color = self.img.pixel[
                                int(tex_pos[0] * self.img.image_width), int(tex_pos[1] * self.img.image_height)][:3]

                    view_dir = ti.Vector([cam_posx - fragment_pos[0], cam_posy - fragment_pos[1], cam_posz - fragment_pos[2]]).normalized()

                    frag_color = self.fragment_shader(normal, color, view_dir, fragment_pos)

                    # set buffer
                    # temp = buffer(depth=depth_pos,
                    #               color=frag_color,
                    #               normal=normal,
                    #               texcoord=tex_pos,
                    #               frag_pos=fragment_pos,
                    #               index=index)

                    set_buffer(x, y, frag_color, depth_pos)

                    # set_buffer(x, y, temp)

    @ti.func
    def fragment_shader(self, normal, obj_color, viewdir, frag_pos):
        # update

        norm = ti.math.normalize(normal)
        view = ti.math.normalize(viewdir)

        result = ti.Vector([0.0, 0.0, 0.0])

        for index in range(LightComponent.len):
            if LightComponent.ti_light[index].render:
                if LightComponent.ti_light[index].type == 1:  # point light type
                    # position, color, mtl : ambient, diffuse, specular, shineness
                    # parm : constant, linear, quadratic

                    lightDir = LightComponent.ti_light[index].position - frag_pos[:3]
                    distance = ti.math.length(lightDir)
                    lightDir = lightDir / distance

                    # diffuse shading
                    diff = max(ti.math.dot(lightDir, norm), 0.0)

                    # specular shading
                    reflectDir = ti.math.reflect(-lightDir, norm)  # x - 2.0 * dot(x, n) * n
                    spec = ti.math.pow(max(ti.math.dot(view, reflectDir), 0.0),
                                       LightComponent.ti_light[index].mtl[3])

                    # attenuation
                    attenuation = 1.0 / (LightComponent.ti_light[index].parm[0] +
                                         LightComponent.ti_light[index].parm[1] * distance +
                                         LightComponent.ti_light[index].parm[2] * distance * distance)

                    ambient = LightComponent.ti_light[index].mtl[0] * obj_color / 255 * attenuation

                    diffuse = LightComponent.ti_light[index].mtl[1] * diff * obj_color / 255 * attenuation

                    specular = LightComponent.ti_light[index].mtl[2] * spec * obj_color / 255 * attenuation

                    result += ambient + diffuse + specular

                if LightComponent.ti_light[index].type == 2:
                    lightDir = (-1) * ti.math.normalize(LightComponent.ti_light[index].position)
                    diff = max(ti.math.dot(lightDir, norm), 0.0)
                    reflectDir = ti.math.reflect(-lightDir, norm)  # x - 2.0 * dot(x, n) * n
                    spec = ti.math.pow(max(ti.math.dot(view, reflectDir), 0.0),
                                       LightComponent.ti_light[index].mtl[3])

                    surface_color = ti.Vector([obj_color[0] * LightComponent.ti_light[index].color[0],
                                               obj_color[1] * LightComponent.ti_light[index].color[1],
                                               obj_color[2] * LightComponent.ti_light[index].color[2]])

                    ambient = LightComponent.ti_light[index].mtl[0] * surface_color
                    diffuse = LightComponent.ti_light[index].mtl[1] * diff * surface_color
                    specular = LightComponent.ti_light[index].mtl[2] * spec * surface_color

                    result += ambient + diffuse + specular

        return result
