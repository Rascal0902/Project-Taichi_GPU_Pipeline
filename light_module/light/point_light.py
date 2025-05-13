import taichi as ti


class PointLight:
    def __init__(self):
        self.position = None
        self.light_color = ti.Vector([1.0, 1.0, 1.0])

        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.shineness = None

        self.constant = None
        self.linear = None
        self.quadratic = None

        self.render = True

    def set_position(self, position):
        self.position = position

    def set_light_color(self, lightcolor):
        self.light_color = lightcolor

    def set_mtl(self, ambient, diffuse, specular, shineness):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shineness = shineness

    def set_parameter(self, constant, linear, quadratic):
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic

    def switch(self, boolean: bool):
        self.render = boolean

    def light_info(self):
        print(f"position: {self.position}")
        print(f"ambient: {self.ambient}")
        print(f"diffuse: {self.diffuse}")
        print(f"specular: {self.specular}")
        print(f"shineness: {self.shineness}")
