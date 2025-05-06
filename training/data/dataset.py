import os
import cv2
import json
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset
from configparser import ConfigParser as CP
from torchvision.transforms import transforms

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

DATASET_VERSION = config.get("model_training","dataset_version")
DATA_DIR = os.path.join(os.getcwd(),"training/data/training_data",DATASET_VERSION)
with open(os.path.join(os.getcwd(),"training/data/templates/template_shapes.json"),"r") as of:
    js_dict = json.load(of)
    COLORS = [c["color"] for c in js_dict.values()]


class TrainingDataset(Dataset):
    def __init__(self):
        self.images = [os.path.join(DATA_DIR,img) for img in os.listdir(DATA_DIR)]
        self.img_transforms = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor()
        ])
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        
        img = cv2.imread(img_path)
        mask = cv2.imread(img_path)
        masks = [self.extract_color(mask, color) for color in COLORS]
        
        img = self.img_transforms(self.make_black(img))
        mask = torch.stack([torch.from_numpy(mask).float() for mask in masks],dim=0)
        
        return (img,mask)
    
    def make_black(self,image):
        mask = np.all(image == [255,255,255],axis=-1)
        img_b_w = np.zeros(image.shape[:2],dtype=np.uint8)
        img_b_w[mask] = 255
        return Image.fromarray(img_b_w)

    def extract_color(self,image,color):
        '''color in hex'''
        color = [int(color[i:i+2],16) for i in (1,3,5)]
        mask = np.all(image == color,axis=-1)
        img_b_w = np.zeros(image.shape[:2],dtype=np.uint8)
        img_b_w[mask] = 1
        return img_b_w