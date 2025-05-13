import taichi as ti


class DirectLight:

    def __init__(self):
        self.direction = None
        self.light_color = ti.Vector([1, 1, 1])

        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.shineness = None

        self.render = True

    def set_direction(self, direction):
        self.direction = direction

    def set_light_color(self, lightcolor):
        self.light_color = lightcolor

    def set_mtl(self, ambient, diffuse, specular, shineness):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shineness = shineness

    def switch(self, boolean: bool):
        self.render = boolean

    def light_info(self):
        print(f"direction: {self.direction}")
        print(f"ambient: {self.ambient}")
        print(f"diffuse: {self.diffuse}")
        print(f"specular: {self.specular}")
        print(f"shineness: {self.shineness}")