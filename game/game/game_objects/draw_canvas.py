from PIL import Image
import pygame
from configparser import ConfigParser as CP
import os
import ast

config = CP()
config.read(os.path.join(os.getcwd(), "etc", ".conf"))

CANVAS_SIZE = ast.literal_eval(config.get("game", "player_canvas_size"))
MODEL_IMG_SIZE = ast.literal_eval(config.get("create_data", "img_size"))


def image_to_surface(img:Image.Image):
    img = img.resize(CANVAS_SIZE) # reshape the image
    return pygame.image.frombytes(img.tobytes(),img.size,img.mode).convert_alpha()

def surface_to_image(surface:pygame.Surface):
    img = Image.frombytes("RGB",surface.get_size(),pygame.image.tobytes(surface,"RGB"))
    img = img.resize(MODEL_IMG_SIZE) # resize for model usage
    return img

