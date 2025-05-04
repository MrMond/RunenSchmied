import torch
from torch.nn import Module
import os
import ast
import tqdm # for progress bar visualization
from configparser import ConfigParser as CP

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

MODEL_VERSION = config.get("model_training","model_version")

class UNet(Module):
    def __init__(self):
        super().__init__()
    
        # Encoder
        
        
        # Decoder
    
    def forward(self,x):
        # Encoder
        
        # Decoder
    
        pass