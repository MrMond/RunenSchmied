from configparser import ConfigParser as CP
import os
import ast
import torch
import segmentation_models_pytorch as smp

# relative imports
from model.training import train_model

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

MODEL_VERSION = config.get("model_training","model_version")
MODEL_PATH = os.path.join(os.getcwd(),"training/model/models",f"transfer_{MODEL_VERSION}.pth")
ENCODER =  config.get("transfer_learning","encoder_name")
WEIGHTS = config.get("transfer_learning","encoder_weights")
N_CLASSES = ast.literal_eval(config.get("model_training","n_classes"))

if __name__ == "__main__":
    # create necessairy objects
    model = smp.Unet(
        encoder_name=ENCODER,
        encoder_weights=WEIGHTS,
        in_channels=1,
        classes=N_CLASSES
    )
    
    model = train_model(model)
    
    #save model
    model.eval() # freeze model weights
    torch.save(model.state_dict(),MODEL_PATH)