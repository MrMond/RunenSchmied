import pygame

pygame.init() # the following imports require initialized pygame environment

from game.window import draw_state
from game.event_handler import handle_events
from game.game_state import SCENEMANAGER

if __name__ == "__main__":
    
    while True:
        
        scene = SCENEMANAGER.get_active_scene()
        
        draw_state(scene)
        
        scene.step() # accept player inputs
                
        handle_events(scene)