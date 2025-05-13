import taichi as ti


class ImageManager:
    def __init__(self):
        self.path = None
        self.img = None

        self.image_width = None
        self.image_height = None
        self.pixel = None

    def loadImage(self, path):
        self.path = path
        self.img = ti.tools.image.imread(self.path)
        self.pixel = ti.Vector.field(4, dtype=ti.f32, shape=(self.img.shape[0], self.img.shape[1]))
        self.image_width = self.img.shape[0]
        self.image_height = self.img.shape[1]
        self.pixel.from_numpy(self.img)
