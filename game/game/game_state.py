import pygame
from PIL import Image
from game.game_objects.player import get_player
from game.game_objects.stats_state import get_stats_from_image
from configparser import ConfigParser as CP
import os
import ast

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

SCREEN_SIZE = ast.literal_eval(config.get("game","screen_size"))

class Drawable:
    def draw(self,screen:pygame.Surface):
        raise NotImplementedError()

class Player(Drawable):
    def __init__(self,player:pygame.Rect, color:tuple):
        self.player = player
        self.color = color
    
    def draw(self,screen:pygame.Surface):
        pygame.draw.rect(screen,self.color,self.player)

class TextDisplay(Drawable):
    def __init__(self,text:str,text_color:tuple,background_color:tuple,center_position:tuple):
        self.txt_col = text_color
        self.bgr_col = background_color
        self.font = pygame.font.Font("freesansbold.ttf",32)
        self.text = self.font.render(text,True,text_color,background_color)
        self.rect = self.text.get_rect()
        self.rect.center = center_position
        
    def set_display(self,img:Image):
        stats = get_stats_from_image(img)
        text = "\n".join([f"{key}\n{value}" for key, value in stats.items()])
        self.text = self.font.render(text,True,self.txt_col,self.bgr_col)
        self.rect = self.text.get_rect()
    
    def draw(self, screen):
        screen.blit(self.text,self.rect)

# game-objets
PLAYER = Player(*get_player())
STATS_DISPLAY = TextDisplay("",(0,255,0),(0,0,0),(SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2))

# getters
def get_objects()->dict[str,Drawable]:
    return {"player":PLAYER,"stats":STATS_DISPLAY}
