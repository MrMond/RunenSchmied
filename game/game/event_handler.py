import pygame
from game.game_state import get_objects

def handle_events():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                close_game()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_r: # r to refresh stats
                        get_objects()["stats"].set_display(None)

def close_game():
    pygame.quit()
    quit()