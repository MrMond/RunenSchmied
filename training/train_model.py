import torch
import os
import ast
from tqdm import tqdm # for progress bar visualization
from configparser import ConfigParser as CP
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn

# relative imports
from model.training import train_model
from model.model_definition import UNet

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

MODEL_VERSION = config.get("model_training","model_version")
MODEL_PATH = os.path.join(os.getcwd(),"training/model/models",f"{MODEL_VERSION}.pth")

if __name__ == "__main__":
    # create necessairy objects
    model = UNet()
    try:
        model.load_state_dict(torch.load(MODEL_PATH,weights_only=True)) 
    except:
        print(f"No Model state found for {MODEL_VERSION}")
        
    model = train_model(model)
    
    #save model
    model.eval() # freeze model weights
    torch.save(model.state_dict(),MODEL_PATH)