import torch
import os
import ast
from tqdm import tqdm # for progress bar visualization
from configparser import ConfigParser as CP
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn

# relative imports
from data.dataset import TrainingDataset
from model.model_definition import UNet

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

DATASET_VERSION = config.get("model_training","dataset_version")
MODEL_VERSION = config.get("model_training","model_version")
MODEL_PATH = os.path.join(os.getcwd(),"training/model/models",f"{MODEL_VERSION}.pth")
BATCH_SIZE = ast.literal_eval(config.get("model_training","batch_size"))
N_EPOCHS = ast.literal_eval(config.get("model_training","n_epochs"))
LR = ast.literal_eval(config.get("model_training","learning_rate"))
PATIENCE = ast.literal_eval(config.get("model_training","schedule_patience"))

if __name__ == "__main__":
    # create necessairy objects
    model = UNet()
    dataset = TrainingDataset()
    loader = DataLoader(dataset,batch_size=BATCH_SIZE, shuffle=True)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(),lr=LR)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer,patience=PATIENCE)
    
    # activate GPU if possible
    d = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {d}")
    device = torch.device(d)
    model.to(device)
    
    # train model
    epoch_loss = 0
    
    for epoch in tqdm(range(N_EPOCHS),"Training model (epochs)"):
        for batch_x,batch_y in loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            preds= model(batch_x)
            loss = loss_fn(preds,batch_y)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        
        scheduler.step(epoch_loss / len(loader))
        
        if epoch+1 % 5 == 0:
            print(f"epoch: {epoch}: Loss = {loss.item()}")
    
    #save model
    model.eval() # freeze model weights
    torch.save(model.state_dict(),MODEL_PATH)