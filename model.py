import torch
from torch import nn


def isru(x):
    return x / torch.sqrt(1 + x * x)


class Generator(nn.Module):
    def __init__(self):
        super().__init__()

        ngf = 96

        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(128, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.PReLU(),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.PReLU(),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.PReLU(),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.PReLU(),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(ngf, ngf // 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf // 2),
            nn.PReLU(),
            nn.ConvTranspose2d(ngf // 2, 3, 4, 2, 1, bias=False)
            # state size. (nc) x 64 x 64
        )

    def forward(self, z):
        z = z.reshape(-1, 128, 1, 1)
        return 0.5 + 0.5 * isru(self.main(z))