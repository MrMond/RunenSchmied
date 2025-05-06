import os
import ast
import torch
import torch.nn as nn
from torch.nn.functional import relu
from configparser import ConfigParser as CP

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

KS = ast.literal_eval(config.get("model_training","kernel_size"))
PD = KS//2
MODEL_VERSION = config.get("model_training","model_version")
N_CLASSES = ast.literal_eval(config.get("model_training","n_classes"))

class UNet(nn.Module):
    def __init__(self):
        super().__init__()
    
        ################# Encoder #################
        
        # 2x convolutional(p:1,k:3x3): 1Filter@(1008x208) --> 64F@(1008x208) --> 64F@(1008x208)
        
        self.level1_down_conv1 = nn.Conv2d(in_channels=1,out_channels=64,kernel_size=KS,padding=PD)
        self.level1_down_conv2 = nn.Conv2d(in_channels=64,out_channels=64,kernel_size=KS,padding=PD)
        
        # 1x max pool 2x2 - (1008x208)
        
        self.level1_down_pool = nn.MaxPool2d(kernel_size=2,stride=2)
        
        # 2x convolutional(p:1,k:3x3): 64F@(504x104) --> 128F@(504x104) --> 128F@(504x104)
        
        self.level2_down_conv1 = nn.Conv2d(in_channels=64,out_channels=128,kernel_size=KS,padding=PD)
        self.level2_down_conv2 = nn.Conv2d(in_channels=128,out_channels=128,kernel_size=KS,padding=PD)
        
        # 1x max pool 2x2 - (504x104)
        
        self.level2_down_pool = nn.MaxPool2d(kernel_size=2,stride=2)
        
        # 2x convolutional(p:1,k:3x3): 128F@(252x52) --> 256F@(252x52) --> 256F@(252x52)
        
        self.level3_down_conv1 = nn.Conv2d(in_channels=128,out_channels=256,kernel_size=KS,padding=PD)
        self.level3_down_conv2 = nn.Conv2d(in_channels=256,out_channels=256,kernel_size=KS,padding=PD)
        
        # 1x max pool 2x2 - (252x52)
        
        self.level3_down_pool = nn.MaxPool2d(kernel_size=2,stride=2)
        
        # 2x convolutional(p:1,k:3x3): 256F@(126x26) --> 512F@(126x26) --> 512@(126x26)
        
        self.level4_down_conv1 = nn.Conv2d(in_channels=256,out_channels=512,kernel_size=KS,padding=PD)
        self.level4_down_conv2 = nn.Conv2d(in_channels=512,out_channels=512,kernel_size=KS,padding=PD)
        
        ################# Decoder #################
        
        # 1x up-conv 2x2 - (126x26)
        
        self.level4_up_conv = nn.ConvTranspose2d(in_channels=512,out_channels=256,kernel_size=2,stride=2)
        
        # 2x convolutional(p:1,k:3x3): 512F@(252x52) --> 256F@(252x52) --> 256F@(252x52)
        
        self.level3_up_conv1 = nn.Conv2d(in_channels=512,out_channels=256,kernel_size=KS,padding=PD)
        self.level3_up_conv2 = nn.Conv2d(in_channels=256,out_channels=256,kernel_size=KS,padding=PD)
        
        # 1x up-conv 2x2 - (252x52)
        
        self.level3_up_conv = nn.ConvTranspose2d(in_channels=256,out_channels=128,kernel_size=2,stride=2)
        
        # 2x convolutional(p:1,k:3x3): 256F@(504x104) --> 128F@(504x104) --> 128F@(504x104)
        
        self.level2_up_conv1 = nn.Conv2d(in_channels=256,out_channels=128,kernel_size=KS,padding=PD)
        self.level2_up_conv2 = nn.Conv2d(in_channels=128,out_channels=128,kernel_size=KS,padding=PD)
        
        # 1x up-conv 2x2 - (504x104)
        
        self.level2_up_conv = nn.ConvTranspose2d(in_channels=128,out_channels=64,kernel_size=2,stride=2)
        
        # 3x convolutional(p:1,k:3x3): 128F@(1008x208) --> 64F@(1008x208) --> 64F@(1008x208) - (p:0,k:1x1)-> nclasses F@(1008x208)
        
        self.level1_up_conv1 = nn.Conv2d(in_channels=128,out_channels=64,kernel_size=KS,padding=PD)
        self.level1_up_conv2 = nn.Conv2d(in_channels=64,out_channels=64,kernel_size=KS,padding=PD)
        self.level1_up_conv3 = nn.Conv2d(in_channels=64,out_channels=N_CLASSES,kernel_size=1) # output layer
    
    def forward(self,x):
        ################# Encoder #################
        
        # level 1
        
        x_l1d1 = relu(self.level1_down_conv1(x))
        x_l1d2 = relu(self.level1_down_conv2(x_l1d1))
        
        # pool
        
        x_l1p = self.level1_down_pool(x_l1d2)
        
        # level 2
        
        x_l2d1 = relu(self.level2_down_conv1(x_l1p))
        x_l2d2 = relu(self.level2_down_conv2(x_l2d1))
        
        # pool
        
        x_l2p = self.level2_down_pool(x_l2d2)
        
        # level 3
        
        x_l3d1 = relu(self.level3_down_conv1(x_l2p))
        x_l3d2 = relu(self.level3_down_conv2(x_l3d1))
        
        # pool
        
        x_l3p = self.level3_down_pool(x_l3d2)
        
        # level 4
        
        x_l4d1 = relu(self.level4_down_conv1(x_l3p))
        x_l4d2 = relu(self.level4_down_conv2(x_l4d1))
        
        ################# Decoder #################
        
        # upconv
        
        x_l4u = self.level4_up_conv(x_l4d2)
        
        # level 3
        
        x_l3u1 = relu(self.level3_up_conv1(torch.cat([x_l4u,x_l3d2],dim=1))) # cat is for "skip" connection
        x_l3u2 = relu(self.level3_up_conv2(x_l3u1))
        
        # upconv
        
        x_l3u = self.level3_up_conv(x_l3u2)
        
        # level 2
        
        x_l2u1 = relu(self.level2_up_conv1(torch.cat([x_l3u,x_l2d2],dim=1)))
        x_l2u2 = relu(self.level2_up_conv2(x_l2u1))
        
        # upconv
        
        x_l2u = self.level2_up_conv(x_l2u2)
        
        # level 1
        
        x_l1u1 = relu(self.level1_up_conv1(torch.cat([x_l2u,x_l1d2],dim=1)))
        x_l1u2 = relu(self.level1_up_conv2(x_l1u1))
        x_l1u3 = relu(self.level1_up_conv3(x_l1u2)) # 1x1 conv for output
    
        return x_l1u3