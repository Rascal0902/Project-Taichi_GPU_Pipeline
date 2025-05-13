import torch
import torch.nn as nn
from collections import OrderedDict
import torch.nn.functional as F

from light_module.Gardner2019.DenseBlock import _DenseBlock
from light_module.Gardner2019.Transition import _Transition


class ParamLENet(nn.Module):
    def __init__(self, growth_rate=32, block_config=(6, 12, 24, 16),
                 num_init_features=64, bn_size=4, drop_rate=0, latent_size=3072, decode_size=512, num_lights=10,
                 memory_efficient=False):

        super(ParamLENet, self).__init__()

        # First convolution
        self.features = nn.Sequential(OrderedDict([
            ('conv0', nn.Conv2d(3, num_init_features, kernel_size=7, stride=2,
                                padding=3, bias=False)),
            ('norm0', nn.BatchNorm2d(num_init_features)),
            ('relu0', nn.ReLU(inplace=True)),
            ('pool0', nn.MaxPool2d(kernel_size=3, stride=2, padding=1)),
        ]))

        # Each denseblock
        num_features = num_init_features
        for i, num_layers in enumerate(block_config):
            block = _DenseBlock(
                num_layers=num_layers,
                num_input_features=num_features,
                bn_size=bn_size,
                growth_rate=growth_rate,
                drop_rate=drop_rate,
                memory_efficient=memory_efficient
            )
            self.features.add_module('denseblock%d' % (i + 1), block)
            num_features = num_features + num_layers * growth_rate
            if i != len(block_config) - 1:
                trans = _Transition(num_input_features=num_features,
                                    num_output_features=num_features // 2)
                self.features.add_module('transition%d' % (i + 1), trans)
                num_features = num_features // 2

        self.latent = nn.Linear(num_features, latent_size)

        self.decoder = nn.Linear(latent_size, decode_size)

        self.l_out = nn.Linear(decode_size, 3 * num_lights)
        self.s_out = nn.Linear(decode_size, num_lights)
        self.c_out = nn.Linear(decode_size, 3 * num_lights)
        self.a_out = nn.Linear(decode_size, 3)
        self.d_out = nn.Linear(latent_size + 3 * num_lights, num_lights)

    def forward(self, x):
        features = self.features(x)
        out = F.relu(features, inplace=True)
        out = F.adaptive_avg_pool2d(out, (1, 1))  # output: 1*1, average pooling over full feature map
        out = torch.flatten(out, 1)  # flatten: keep some dims and merge the others
        # replace the classifier with two FC layers
        latent_vec = self.latent(out)
        decode_vec = self.decoder(latent_vec)

        # !!! ------ issue here ------ !!!
        # d = self.d_out(decode_vec)  # [3], 3 float
        l = self.l_out(decode_vec)  # [9], 3 vec
        s = self.s_out(decode_vec).clamp_min(0.0001)  # [3], 3 float
        c = self.c_out(decode_vec).clamp_min(0.0)  # [9], 3 vec
        a = self.a_out(decode_vec).clamp_min(0.0)  # [3], 1 vec
        z_l_cat = torch.cat([latent_vec, l], dim=1)
        d = self.d_out(z_l_cat).clamp_min(0.0001)
        # !!! ------ issue here ------ !!!
        return [d, l, s, c, a]
