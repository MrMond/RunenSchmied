import torch
import os
import ast
from tqdm import tqdm # for progress bar visualization
from configparser import ConfigParser as CP
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn
from tempfile import TemporaryDirectory

from data.dataset import TrainingDataset

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

BATCH_SIZE = ast.literal_eval(config.get("model_training","batch_size"))
NUM_WORKERS = ast.literal_eval(config.get("model_training","batch_size"))
N_EPOCHS = ast.literal_eval(config.get("model_training","n_epochs"))
LR = ast.literal_eval(config.get("model_training","learning_rate"))
PATIENCE = ast.literal_eval(config.get("model_training","schedule_patience"))


def train_model(model:nn.Module)->nn.Module: # after https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
    
    dataset = TrainingDataset()
    dataloader = DataLoader(dataset,batch_size=BATCH_SIZE,shuffle=True,num_workers=NUM_WORKERS)
    dataset_size = len(dataset)
    
    d = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {d}")
    device = torch.device(d)
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(),lr=LR)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer,patience=PATIENCE)
    
    with TemporaryDirectory() as tmpdir:
        best_model_params_path = os.path.join(tmpdir,"best_model_params.pt")
        torch.save(model.state_dict(),best_model_params_path)
        best_acc = 0
        
        for epoch in tqdm(range(N_EPOCHS),"Training model (epoch)"):
            for phase in ["train","val"]:
                if phase == "train": # switch training / evaluation mode
                    model.train()
                else:
                    model.eval()
                    
                running_loss = 0
                running_corrects = 0
                
                for inputs, labels in dataloader:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
                    
                    optimizer.zero_grad()
                    
                    with torch.set_grad_enabled(phase == "train"):
                        outputs = model(inputs) # one-hot encoded output
                        _, predictions = torch.max(outputs,1) # torch.max reduces dim1 --> shape looses class dimension
                        loss = criterion(outputs,labels) # one-hot-encoded labels
                        
                        if phase == "train": # backward pass        
                            loss.backward()
                            optimizer.step()
                    
                    running_loss += loss.item() * inputs.size(0)
                    labels = torch.argmax(labels,dim=1) # assert dimensions of labels == predictions
                    running_corrects += torch.sum(predictions == labels.data)
                
                epoch_loss = running_loss/dataset_size
                epoch_acc = running_corrects.double()/dataset_size #type:ignore
                
                if phase == "train":
                    scheduler.step(epoch_loss)
                
                if epoch+1%5==0 or epoch == 0:
                    print(f"\n{epoch+1}({phase}) Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
                
                if phase == "val" and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    torch.save(model.state_dict(),best_model_params_path)
        model.load_state_dict(torch.load(best_model_params_path,weights_only=True))
        return model