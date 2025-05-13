import taichi as ti


# buffer = ti.types.struct(
#     depth=ti.f64,
#     color=ti.math.vec3,
#     normal=ti.math.vec3,
#     texcoord=ti.math.vec2,
#     frag_pos=ti.math.vec4,
#     index=ti.i32)


@ti.data_oriented
class Storage:
    def __init__(self, w, h):
        Storage.w, Storage.h = w, h
        # Storage.buffer_array = buffer.field(shape=(w, h))

        # Storage.camera = None

        Storage.z_buffer = ti.field(dtype=ti.f64, shape=(w, h))
        Storage.pixel = ti.Vector.field(3, dtype=ti.f32, shape=(w, h))

        # self._buffer = buffer(depth=-1000.0,
        #                  color=ti.Vector([1.0, 1.0, 1.0]),
        #                  normal=ti.Vector([1.0, 0.0, 0.0]),
        #                  texcoord=ti.Vector([-1.0, -1.0]),
        #                  frag_pos=ti.Vector([-1.0, -1.0, -1.0, 1.0]),
        #                  index=-1)

    # def setCamera(self, camera):
    #     Storage.camera = camera

    # @ti.kernel
    # def initialize_buffer_array(self):
    #     for i, j in ti.ndrange(Storage.w, Storage.h):
    #         Storage.buffer_array[i, j] = self._buffer

    @ti.kernel
    def initialize_window(self):
        for i, j in ti.ndrange(Storage.w, Storage.h):
            Storage.z_buffer[i, j] = -1000.0
            Storage.pixel[i, j] = ti.Vector([1.0, 1.0, 1.0])

    def get_pixel(self):
        return Storage.pixel


@ti.func
def tri_area(v1_2d: ti.math.vec2, v2_2d: ti.math.vec2, v3_2d: ti.math.vec2):
    area = (v2_2d[0] - v1_2d[0]) * (v3_2d[1] - v1_2d[1]) - \
           (v3_2d[0] - v1_2d[0]) * (v2_2d[1] - v1_2d[1])
    return area


@ti.func
def barycentric_coord(p: ti.math.vec2, v0: ti.math.vec2, v1: ti.math.vec2, v2: ti.math.vec2):
    area = tri_area(v0, v1, v2) + 1e-8  # make safe
    w0 = tri_area(p, v1, v2) / area
    w1 = tri_area(p, v2, v0) / area
    w2 = tri_area(p, v0, v1) / area
    return ti.math.vec3(w0, w1, w2)


@ti.func
def set_buffer(x, y, color, depth):  # color buffer
    if depth > Storage.z_buffer[x, y]:
        Storage.z_buffer[x, y] = depth
        Storage.pixel[x, y] = color


# @ti.func
# def set_buffer(x, y, buf):
#     if buf.depth > Storage.z_buffer[x, y]:
#         Storage.buffer_array[x, y] = buf
#         Storage.z_buffer[x, y] = buf.depth
#
#     if Storage.buffer_array[x, y].index == -1 and buf.depth > Storage.z_buffer[x, y]:
#         Storage.buffer_array[x, y] = buf
#         Storage.z_buffer[x, y] = buf.depth

# @ti.func
# def set_buffer(x, y, buf):
#     if Storage.buffer_array[x, y, 0].index == -1 and buf.depth > Storage.z_buffer[x, y]:
#         Storage.buffer_array[x, y, 0] = buf
#         Storage.z_buffer[x, y] = buf.depth
#     else:
#         if Storage.buffer_array[x, y, 0].depth < buf.depth:
#             Storage.buffer_array[x, y, 1] = Storage.buffer_array[x, y, 0]
#             Storage.buffer_array[x, y, 0] = buf
#             Storage.z_buffer[x, y] = buf.depth
#         else:
#             if Storage.buffer_array[x, y, 1].index == -1:
#                 Storage.buffer_array[x, y, 1] = buf
#             else:
#                 if Storage.buffer_array[x, y, 1].depth < buf.depth:
#                     Storage.buffer_array[x, y, 1] = buf

@ti.kernel
def z_buffering():
    for x, y in ti.ndrange(Storage.w, Storage.h):
        if Storage.buffer_array[x, y].index != -1 and Storage.z_buffer[x, y] <= Storage.buffer_array[x, y].depth:
            frag_color = Storage.buffer_array[x, y].color
            Storage.pixel[x, y] = frag_color

# @ti.kernel
# def z_buffering():
#     for x, y in ti.ndrange(Storage.w, Storage.h):
#         if Storage.buffer_array[x, y, 0].index != -1 and Storage.z_buffer[x, y] <= Storage.buffer_array[x, y, 0].depth:
#             if Storage.buffer_array[x, y, 1].index != -1 and Storage.buffer_array[x, y, 1].depth > \
#                     Storage.buffer_array[x, y, 0].depth:
#                 Storage.buffer_array[x, y, 0] = Storage.buffer_array[x, y, 1]
#                 Storage.z_buffer[x, y] = Storage.buffer_array[x, y, 0].depth
#
#             frag_color = Storage.buffer_array[x, y, 0].color
#             Storage.pixel[x, y] = frag_color
