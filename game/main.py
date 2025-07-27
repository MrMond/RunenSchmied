from util_classes import UI_Element,Canvas
import pygame
from configparser import ConfigParser as CP
import os
import ast

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))
SCREEN_SIZE = ast.literal_eval(config.get("game","screen_size"))

pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
SCREEN.fill((100, 110, 125))
pygame.display.set_caption("Runenschmied")

screen_elements = {"canvas":Canvas(SCREEN.get_rect().center)}
mouse_held = False

while True:
    for element in screen_elements.values(): # draw all visible elements
        element.draw(SCREEN)
    pygame.display.update()
    # handle inputs:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                quit()
            case pygame.MOUSEBUTTONDOWN:
                screen_elements["canvas"].update_player_canvas(pygame.mouse.get_pos(),mouse_held) # draw on canvas
                screen_elements["canvas"].update_background_canvas()
                mouse_held = True
            case pygame.MOUSEMOTION:
                if mouse_held:
                    screen_elements["canvas"].update_player_canvas(pygame.mouse.get_pos(),mouse_held) # draw on canvas
                    screen_elements["canvas"].update_background_canvas()
            case pygame.MOUSEBUTTONUP:
                mouse_held = False