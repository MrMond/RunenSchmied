import pygame
from game.game_state import Scene,ImageInput,Interactable

def handle_events(scene:Scene):
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                close_game()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_e:
                        interactable = scene.get_closest_interactable()
                        if isinstance(interactable,Interactable):
                            interactable.interact()
                        if isinstance(scene,ImageInput):
                            scene.on_exit()
                    case pygame.K_ESCAPE:
                        if isinstance(scene,ImageInput):
                            scene.on_exit()
                    case pygame.K_SPACE:
                        if isinstance(scene,ImageInput):
                            scene.use_img()
            case pygame.MOUSEBUTTONDOWN:
                scene.mouse_held = True
                if isinstance(scene,ImageInput):
                    scene.get_objects()["canvas"].interact()
            case pygame.MOUSEBUTTONUP:
                scene.mouse_held = False
            case pygame.MOUSEMOTION:
                if isinstance(scene,ImageInput):
                    if scene.mouse_held:
                        scene.get_objects()["canvas"].interact()

def close_game():
    pygame.quit()
    quit()