import torch
from torch.utils.data import DataLoader

import os
from light_module.Gardner2019.ParamLENet import ParamLENet
from light_module.Gardner2019.util import InputData, load_ckp


class Validation:
    def __init__(self, ckpt_path, N, MODE=None):
        self.MODE = MODE

        self.default_lr = 0.001
        self.device = "cuda:0"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_home_dir = os.path.join(current_dir, "Input_JPG")

        self.model = ParamLENet(num_lights=N).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.default_lr)

        ckp_path = ckpt_path
        _model, _optimizer, _load_epoch = load_ckp(ckp_path, self.model, self.optimizer)

        self.data = InputData(self.MODE)
        self.validation_data_loader = None
        self.model.eval()

    def eval_param(self, Imgdata, PRINT=True):
        self.data.setImage(None, Imgdata)
        self.validation_data_loader = DataLoader(self.data, batch_size=16, pin_memory=True, shuffle=False)

        for batch_idx, sample in enumerate(self.validation_data_loader):
            img_batch = sample["img"].to(self.device)
            estimated_param = self.model(img_batch)
            pred_d = estimated_param[0].to(self.device)  # shape: [N,9]
            pred_l = estimated_param[1].to(self.device)  # shape: [N,9]
            pred_s = estimated_param[2].to(self.device)  # shape: [N,3]
            pred_c = estimated_param[3].to(self.device)  # shape: [N,9]
            pred_a = estimated_param[4].to(self.device)  # shape: [N,3]

        if PRINT is True:
            print('----------------------------------------------')
            # print(f"pred_l : {pred_l}\n")
            print(f"pred_d : {pred_d}\npred_l : {pred_l}\npred_s : {pred_s}\npred_c : {pred_c}\npred_a : {pred_a}")

        return pred_d, pred_l, pred_s, pred_c, pred_a

    def evaltest(self):
        filename = self.data_home_dir + "/9C4A0003-e05009bcad_crop_0_[0.7041082402033767, 2.3557900627137673]_[0.0062814  0.00456242 0.00172713].jpg"
        self.data.setImage(filename, None)
        self.validation_data_loader = DataLoader(self.data, batch_size=6, pin_memory=True, shuffle=False)

        for batch_idx, sample in enumerate(self.validation_data_loader):
            img_batch = sample["img"].to(self.device)
            estimated_param = self.model(img_batch)
            pred_d = estimated_param[0].to(self.device)
            pred_l = estimated_param[1].to(self.device)
            pred_s = estimated_param[2].to(self.device)
            pred_c = estimated_param[3].to(self.device)
            pred_a = estimated_param[4].to(self.device)

        print('----------------------------------------------')
        print(f"pred_d : {pred_d}\npred_l : {pred_l}\npred_s : {pred_s}\npred_c : {pred_c}\npred_a : {pred_a}")
        print("finish")

if __name__ == '__main__':
    ckpt_path = 'ckpt/checkpoint.pt'
    processor = Validation(ckpt_path, N=10, MODE="LIGHT")
    processor.evaltest()
