import pygame
from configparser import ConfigParser as CP
import os
import ast
from game.game_state import Drawable

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

SCREEN_SIZE = ast.literal_eval(config.get("game","screen_size"))
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Runenschmied")

def draw_state(elements:dict[str,Drawable]):
    screen = SCREEN  # define reference in local scope for better performance
    
    screen.fill((0,0,0))
    
    for element in elements.values():
        element.draw(screen)
        
    pygame.display.update()