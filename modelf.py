import torch
import torch.nn as nn

LATENT_CODE_SIZE = 128 # size of the Z vector
SDF_NET_BREADTH = 256 # size of the w vector

amcm = 24 # Autoencoder Model Complexity Multiplier

class Lambda(nn.Module):
    def __init__(self, function):
        super(Lambda, self).__init__()
        self.function = function

    def forward(self, x):
        return self.function(x)

class ModelF(nn.Module):
    def __init__(self):
        super(ModelF, self).__init__()
        self.add_module('encoder', nn.Sequential(
            # Accepts x,y,z, sdf(x,y,z)
            nn.Linear(in_features = 4, out_features = SDF_NET_BREADTH),
            nn.ReLU(inplace=True),

            nn.Linear(in_features = SDF_NET_BREADTH, out_features = SDF_NET_BREADTH),
            nn.ReLU(inplace=True),

            nn.Linear(in_features = SDF_NET_BREADTH, out_features = SDF_NET_BREADTH),
            nn.ReLU(inplace=True),

            nn.Linear(in_features = SDF_NET_BREADTH, out_features = SDF_NET_BREADTH),
            nn.ReLU(inplace=True) 
        ))
        self.cuda()

    def forward(self, psdf):
        psdf = psdf.cuda()
        return self.encoder(psdf)
