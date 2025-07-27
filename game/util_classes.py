from PIL import Image, ImageFilter
import segmentation_models_pytorch as smp
import torch.nn.functional as F
from torchvision import transforms
import torch
import pygame
from configparser import ConfigParser as CP
import os
import ast
import numpy as np
import threading

import pickle

config = CP()
config.read(os.path.join(os.getcwd(), "etc", ".conf"))

CANVAS_SIZE = ast.literal_eval(config.get("game", "player_canvas_size"))
COLORS = ast.literal_eval(config.get("game", "template_color_math")) # {"x":color}
MODEL_IMG_SIZE = ast.literal_eval(config.get("create_data", "img_size"))
MODEL_BOUNDARY = ast.literal_eval(config.get("game", "model_classification_boundary"))
MODEL_VERSION = config.get("game","model_version")
MODEL_PATH = os.path.join(os.getcwd(),f"training/model/models/{MODEL_VERSION}.pth")
MODEL = smp.Unet(
        encoder_name="resnet34",
        encoder_weights="imagenet",
        in_channels=1,
        classes=4
    )
MODEL.load_state_dict(torch.load(MODEL_PATH))
TRANSFORM = transforms.Compose([transforms.Grayscale(num_output_channels=1),transforms.ToTensor()])#transforms.Resize(MODEL_IMG_SIZE),

class Drawable:
    def __init__(self,center_position):
        self.center_position = center_position
    def draw(self,screen:pygame.Surface)->None:
        raise NotImplementedError("Override draw method in child")
    
class Canvas(Drawable):
    def __init__(self,center_position):
        super().__init__(center_position)
        self.background_canvas = self.__init_empty_surface((255,255,255,255))
        self.player_canvas = self.__init_empty_surface((0,0,0,0))
        self.previous=(0,0)
        self.process_lock = threading.Lock()

    def __init_empty_surface(self,b_color:tuple[int,int,int,int])->pygame.Surface:
        '''takes: b_color in RGBA'''
        surface = pygame.Surface(CANVAS_SIZE,pygame.SRCALPHA)
        surface.fill(b_color)
        return surface
    
    def update_player_canvas(self,destination:tuple[int,int],connect_previous=False)->None:
        rect = self.player_canvas.get_rect()
        rect.center = self.center_position
        if rect.collidepoint(*destination):
            x,y = rect.topleft
            corrected_position = destination[0]-x,destination[1]-y
            if connect_previous: # connect a line if mouse is held
                pygame.draw.line(self.player_canvas,(0,0,0,255),self.previous,corrected_position,4)
            else:
                pygame.draw.circle(self.player_canvas,(0,0,0,255),corrected_position,2)
            self.previous = corrected_position

    def update_background_canvas(self)->None:
        def worker():
            try:
                new_background = self.__init_empty_surface((255,255,255,255))
                image = Image.frombytes("RGBA",CANVAS_SIZE,pygame.image.tobytes(self.player_canvas,"RGBA")) # convert surface to image
                image_no_alpha = Image.new("RGB",image.size,(255,255,255)) # white image
                image_no_alpha.paste(image,mask=image.split()[3]) #alpha channel as mask
                prediction = F.softmax(MODEL(TRANSFORM(image_no_alpha).unsqueeze(0)).squeeze(),dim=0) # convert to probabilities
                
                with open("prediction.pkl","wb") as of:
                    pickle.dump(prediction,of)
                image_no_alpha.save("origin.png")
                
                prediction = [prediction[i,:,:] for i in range(len(COLORS))] # iterable through prediction classes
                for color,pred_class in zip(COLORS.values(),prediction): # draw visualization for each class
                    mask = pred_class >= MODEL_BOUNDARY # contains True and False
                    # draw to image: white background & color for lines
                    rgb = np.zeros((*mask.shape,3),dtype=np.uint8)
                    rgb[~mask] = (255,255,255)
                    rgb[mask] = color
                    img = Image.fromarray(rgb,mode="RGB")
                    img = img.resize(CANVAS_SIZE)
                    # thicken lines and blurr a little
                    img = img.filter(ImageFilter.MaxFilter(size=5))
                    img = img.filter(ImageFilter.GaussianBlur(radius=3))
                    # draw to surface
                    channel_mask = pygame.image.frombytes(img.tobytes(),img.size,img.mode).convert_alpha()
                    new_background.blit(channel_mask,(0,0))
                self.background_canvas = new_background
            finally:
                self.process_lock.release()
                print("updated canvas")
        if self.process_lock.acquire(blocking=False):
            threading.Thread(target=worker,daemon=True,).start()

    def draw(self,screen)->None:
        background_rect = self.background_canvas.get_rect()
        background_rect.center = self.center_position
        screen.blit(self.background_canvas,background_rect)
        player_rect = self.player_canvas.get_rect()
        player_rect.center = self.center_position
        screen.blit(self.player_canvas,player_rect)
        
class UI_Element(Drawable):
    def __init__(self,center_position) -> None:
        super().__init__(center_position)