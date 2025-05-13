import torch
from torch.utils.data import Dataset
from torchvision import transforms

import cv2
from PIL import Image

transformer = transforms.Compose([
    transforms.Resize(256),
    transforms.ToTensor()])


class InputData(Dataset):
    def __init__(self, MODE=None):
        self.MODE = MODE
        self.filenames = None
        self.data = None
        self.transformer = transformer  # resize & to tensor

    def __len__(self):
        return 1

    def setImage(self, filename, data):
        if self.MODE == "LIGHT":
            self.filenames = filename

        if self.MODE == "MIX":
            self.data = data

    def __getitem__(self, idx):
        if self.MODE == "LIGHT":
            crop_img_name = self.filenames
            img = Image.open(crop_img_name)  # open jpg file
            img = self.transformer(img)  # [Nc, 3, 256, 256]
            return {'img': img}  # cropped img + light env + ambient

        if self.MODE == "MIX":
            img = self.data
            img = self.transformer(img)
            return {'img': img}


def cv2_to_PIL(img):
    _img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return _img


def load_ckp(fpath, model, optimizer):
    ckp = torch.load(fpath)
    model.load_state_dict(ckp['state_dict'])
    optimizer.load_state_dict(ckp['optimizer'])
    return model, optimizer, ckp['epoch']
