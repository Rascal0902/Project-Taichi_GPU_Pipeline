import taichi as ti
import torch
import numpy as np
import point_cloud_utils as pcu

class MeshLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.obj = None
        self.render = True

        self.verts = None
        self.obj_faces = None
        self.normals = None

    def obj_render(self, boolean: bool):
        self.render = boolean

    def ply_render(self, boolean: bool):
        self.render = boolean

    def obj_load(self):
        vertices = []
        normals = []
        texture_coords = []
        faces = []

        with open(self.filepath, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if parts and parts[0] == 'v':
                    vertex = list(map(float, parts[1:4]))
                    vertices.append(vertex)
                elif parts and parts[0] == 'vt':
                    tex_coord = list(map(float, parts[1:3]))
                    texture_coords.append(tex_coord)
                elif parts and parts[0] == 'vn':
                    normal = list(map(float, parts[1:4]))
                    normals.append(normal)
                elif parts and parts[0] == 'f':
                    face = []
                    for part in parts[1:]:
                        vertex_index = part.split('/')
                        # 0-based index
                        face.append([int(vertex_index[0]) - 1, int(vertex_index[1]) - 1, int(vertex_index[2]) - 1])
                    faces.append(face)

        triangles = []
        for face in faces:
            if len(face) == 4:
                triangles.append([face[0], face[1], face[2]])
                triangles.append([face[2], face[3], face[0]])
            else:
                triangles.append(face)

        self.obj = {
            'vertices': torch.from_numpy(np.array(vertices, dtype=np.float32)).to('cuda'),
            'normals': torch.from_numpy(np.array(normals, dtype=np.float32)).to('cuda'),
            'texcoords': torch.from_numpy(np.array(texture_coords, dtype=np.float32)).to('cuda'),
            'faces': torch.from_numpy(np.array(triangles, dtype=np.int32)).to('cuda')
        }

        self.verts = ti.field(dtype=ti.f32, shape=(self.obj["vertices"].shape[0], 3))
        self.obj_faces = ti.field(dtype=ti.i32, shape=(self.obj["faces"].shape[0], 3, 3))
        self.normals = ti.field(dtype=ti.f32, shape=(self.obj["faces"].shape[0], 3))

        # print("mesh initialized")

    def ply_load(self):
        v, f, c = pcu.load_mesh_vfc(self.filepath)

        self.obj = {
            'vertices': torch.from_numpy(np.array(v, dtype=np.float32)).to('cuda'),
            'colors': torch.from_numpy(np.array(c, dtype=np.float32)).to('cuda'),
            'faces': torch.from_numpy(np.array(f, dtype=np.int32)).to('cuda')
        }

        self.verts = ti.field(dtype=ti.f32, shape=(self.obj["vertices"].shape[0], 3))
        self.obj_faces = ti.field(dtype=ti.i32, shape=(self.obj["faces"].shape[0], 3))
        self.normals = ti.field(dtype=ti.f32, shape=(self.obj["vertices"].shape[0], 3))

        self.verts.from_torch(self.obj["vertices"])
        self.obj_faces.from_torch(self.obj["faces"])

        ply_normal_generator(self.verts, self.obj_faces, self.normals)
        normals = self.normals.to_numpy()
        self.obj['normals'] = torch.from_numpy(np.array(normals, dtype=np.float32)).to('cuda')


    def obj_info(self):
        if self.obj is None:
            print("No mesh loaded")

        print("obj info")
        print(self.obj["vertices"])
        print(self.obj["faces"])
        print(self.obj["normals"])
        print(self.obj["texcoords"])

@ti.kernel
def normal_generator(vertices: ti.template(), faces: ti.template(), normals: ti.template()):
    for index in range(faces.shape[0]):
        for i in range(3):
            faces[index, i, 2] = index

        vector1 = ti.Vector([vertices[faces[index, 0, 0], 0], vertices[faces[index, 0, 0], 1], vertices[faces[index, 0, 0], 2]])
        vector2 = ti.Vector([vertices[faces[index, 1, 0], 0], vertices[faces[index, 1, 0], 1], vertices[faces[index, 1, 0], 2]])
        vector3 = ti.Vector([vertices[faces[index, 2, 0], 0], vertices[faces[index, 2, 0], 1], vertices[faces[index, 2, 0], 2]])

        vector12 = vector2 - vector1
        vector13 = vector3 - vector1
        face_normal = ti.math.cross(vector12, vector13)

        normals[index, 0] = ti.math.normalize(face_normal)[0]
        normals[index, 1] = ti.math.normalize(face_normal)[1]
        normals[index, 2] = ti.math.normalize(face_normal)[2]

@ti.kernel
def ply_normal_generator(vertices: ti.template(), faces: ti.template(), normals: ti.template()):
    for index in range(faces.shape[0]):
        vector1 = ti.Vector([vertices[faces[index, 0], 0], vertices[faces[index, 0], 1], vertices[faces[index, 0], 2]])
        vector2 = ti.Vector([vertices[faces[index, 1], 0], vertices[faces[index, 1], 1], vertices[faces[index, 1], 2]])
        vector3 = ti.Vector([vertices[faces[index, 2], 0], vertices[faces[index, 2], 1], vertices[faces[index, 2], 2]])

        vector12 = vector2 - vector1
        vector13 = vector3 - vector1
        face_normal = ti.math.cross(vector12, vector13)

        normals[faces[index, 0], 0] += face_normal[0];normals[faces[index, 0], 1] += face_normal[1];normals[faces[index, 0], 2] += face_normal[2]
        normals[faces[index, 1], 0] += face_normal[0];normals[faces[index, 1], 1] += face_normal[1];normals[faces[index, 1], 2] += face_normal[2]
        normals[faces[index, 2], 0] += face_normal[0];normals[faces[index, 2], 1] += face_normal[1];normals[faces[index, 2], 2] += face_normal[2]


    for index in range(vertices.shape[0]):
        temp = ti.math.normalize(ti.Vector([normals[index, 0], normals[index, 1], normals[index, 2]]))
        normals[index, 0] = temp[0];normals[index, 1] = temp[1];normals[index, 2] = temp[2]


