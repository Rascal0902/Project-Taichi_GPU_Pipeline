import taichi as ti

from light_module.light.direction_light import DirectLight
from light_module.light.point_light import PointLight

light_buffer = ti.types.struct(
    render=ti.i32,
    type=ti.i32,
    position=ti.math.vec3,  # for Direction Light, position is direction
    color=ti.math.vec3,
    mtl=ti.math.vec4,
    parm=ti.math.vec3
)

# No Light is not allowed

class LightComponent:
    component = {}
    ti_light = None
    len = 0
    rendered_len = 0

    def __init__(self):
        LightComponent.len = 0
        LightComponent.rendered_len = 0
        # print("LightComponent init")

    def addPointlight(self, id):
        LightComponent.len += 1
        LightComponent.rendered_len += 1
        LightComponent.component[id] = PointLight()

    def addDirectlight(self, id):
        LightComponent.len += 1
        LightComponent.rendered_len += 1
        LightComponent.component[id] = DirectLight()

    def setPointInfo(self, id, position, light_color, mtlsetting: tuple, parmsetting: tuple):
        LightComponent.component[id].set_position(position)
        LightComponent.component[id].set_light_color(light_color)
        LightComponent.component[id].set_mtl(*mtlsetting)
        LightComponent.component[id].set_parameter(*parmsetting)

    def setDirectInfo(self, id, direction, light_color, mtlsetting: tuple):
        LightComponent.component[id].set_direction(direction)
        LightComponent.component[id].set_light_color(light_color)
        LightComponent.component[id].set_mtl(*mtlsetting)

    def updateposition(self, id, position):
        if LightComponent.component[id].render is False:
            return

        if id == "pointLight":
            LightComponent.component[id].set_position(position)
            LightComponent.ti_light[0].position = position

        if id == "multipointLight":
            LightComponent.component[id].set_position(position)
            LightComponent.ti_light[1].position = position

    def updatedirection(self, id, direction, N=None):
        if LightComponent.component[id].render is False:
            return

        if id == "directLight":
            LightComponent.component[id].set_direction(direction)
            LightComponent.ti_light[2].position = direction
            return

        if N is not None:
            for i in range(N):
                if id == "Direct" + str(i):
                    LightComponent.component[id].set_direction(direction)
                    LightComponent.ti_light[i].position = direction

    def updateddircolor(self, id, color, N=None):
        if LightComponent.component[id].render is False:
            return

        if id == "directLight":
            LightComponent.component[id].set_light_color(color)
            LightComponent.ti_light[2].color = color
            return

        if N is not None:
            for i in range(N):
                if id == "Direct" + str(i):
                    LightComponent.component[id].set_light_color(color)
                    LightComponent.ti_light[i].color = color


    def switch(self, id, boolean: bool):
        if LightComponent.component[id].render != boolean:
            if boolean:
                LightComponent.rendered_len += 1
            else:
                LightComponent.rendered_len -= 1
        LightComponent.component[id].switch(boolean)

    def printInfo(self, id):
        LightComponent.component[id].light_info()

    def setTaichiInfo(self):
        if LightComponent.rendered_len == 0:
            # print("setTaichiInfo: Nothing")
            return

        LightComponent.ti_light = light_buffer.field(shape=LightComponent.len)

        index = 0
        for key, value in LightComponent.component.items():
            if isinstance(value, PointLight):
                LightComponent.ti_light[index] = light_buffer(
                    render=True if value.render else False,
                    type=1,
                    position=ti.Vector([value.position[0], value.position[1], value.position[2]]),
                    color=ti.Vector([value.light_color[0], value.light_color[1], value.light_color[2]]),
                    mtl=ti.Vector([value.ambient, value.diffuse, value.specular, value.shineness]),
                    parm=ti.Vector([value.constant, value.linear, value.quadratic])
                )

            if isinstance(value, DirectLight):
                LightComponent.ti_light[index] = light_buffer(
                    render=True if value.render else False,
                    type=2,
                    position=ti.Vector([value.direction[0], value.direction[1], value.direction[2]]),
                    color=ti.Vector([value.light_color[0], value.light_color[1], value.light_color[2]]),
                    mtl=ti.Vector([value.ambient, value.diffuse, value.specular, value.shineness]),
                    parm=ti.Vector([0.0, 0.0, 0.0])
                )

            index += 1
        # print("setTaichiInfo")
