import pygame
import os

pygame.init()

from game.event_handler import handle_events
from game.window import SCREEN, draw_state
from game.game_objects.player import player_movement_step
from game.game_state import get_objects

if __name__ == "__main__":
    
    while True:
        
        draw_state(get_objects())
        
        player_movement_step()
        
        handle_events()