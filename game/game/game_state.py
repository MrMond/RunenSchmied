import pygame
from PIL import Image
from game.game_objects.player import get_player
from game.game_objects.stats_state import get_stats_from_image
from game.game_objects.player import player_movement_step
from game.game_objects.draw_canvas import image_to_surface, surface_to_image
from typing import Callable
import math
from configparser import ConfigParser as CP
import os
import ast

config = CP()
config.read(os.path.join(os.getcwd(), "etc", ".conf"))

PLAYER_REACH = ast.literal_eval(config.get("game", "player_reach"))

# objects


class Drawable:
    def draw(self, screen: pygame.Surface):
        raise NotImplementedError()


class Player(Drawable):
    def __init__(self, player: pygame.Rect, color: tuple):
        self.player = player
        self.color = color

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.player)

    def set_color(self, color):
        self.color = color


class TextDisplay(Drawable):
    def __init__(
        self,
        text: str,
        text_color: tuple,
        background_color: tuple,
        center_position: tuple,
    ):
        self.txt_col = text_color
        self.bgr_col = background_color
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.text = self.font.render(text, True, text_color, background_color)
        self.rect = self.text.get_rect()
        self.rect.center = center_position

    def set_display(self, img: Image):
        stats = get_stats_from_image(img)
        text = "   ".join([f"{key}: {value}" for key, value in stats.items()])
        self.text = self.font.render(text, True, self.txt_col, self.bgr_col)
        self.rect = self.text.get_rect()

    def draw(self, screen):
        screen.blit(self.text, self.rect)


class Interactable(Drawable):
    def __init__(
        self, dimensions: tuple, color: tuple, player: Player, on_interact: Callable
    ):
        self.rect = pygame.Rect(*dimensions)
        self.color = color
        self.in_range = False
        self.player = player
        self.on_interact = on_interact

    def draw(self, screen: pygame.Surface):
        s_x, s_y = self.rect.center
        p_x, p_y = self.player.player.center
        self.in_range = math.hypot(s_x - p_x, s_y - p_y) <= PLAYER_REACH

        pygame.draw.rect(screen, self.color, self.rect)

        if self.in_range:
            font = pygame.font.Font("freesansbold.ttf", 32)
            font_col = [abs(col - 255) for col in self.color]
            text = font.render("[E]", True, font_col, self.color)
            t_rect = text.get_rect()
            t_rect.center = self.rect.center
            screen.blit(text, t_rect)

    def interact(self):
        if not self.in_range:
            return
        self.on_interact(None)


class Canvas(Drawable):

    def __init__(self):
        self.img_surface = None
        
    def interact(self):
        if not isinstance(self.img_surface,pygame.Surface):
            return
        position = pygame.mouse.get_pos()
        rect = self.img_surface.get_rect()
        rect.center = pygame.display.get_surface().get_rect().center
        if  rect.collidepoint(*position):
            xc,yc = rect.topleft
            corr_pos = position[0]-xc,position[1]-yc
            pygame.draw.circle(self.img_surface,(255,0,0),corr_pos,2)

    def load_img(self,img:Image.Image):
        self.img_surface = image_to_surface(img)
        
    def store_img(self):
        img = surface_to_image(self.img_surface)
        img.save(os.path.join(os.getcwd(), "etc", "mytest.png"))
        return img
        
    def draw(self, screen):
        rect = self.img_surface.get_rect()
        rect.center = pygame.display.get_surface().get_rect().center
        screen.blit(self.img_surface, rect)


# scenes


class Scene:
    def __init__(self, background_color: tuple):
        self.bg_col = background_color
        self.mouse_held = False

    def on_enter(self):
        pass

    def get_objects(self) -> dict[str, Drawable]:
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def get_closest_interactable(self) -> None | Interactable:
        return None


class SceneManager:
    def __init__(self, scenes: list[Scene]):
        self.active_id = 0
        self.scenes = scenes

    def get_active_scene(self) -> Scene:
        return self.scenes[self.active_id]

    def switch_scene(self, new_idx: int):
        self.active_id = new_idx
        self.get_active_scene().on_enter()


class MainGame(Scene):
    """a scene, where the player can move around and"""

    def __init__(self, background_color):
        super().__init__(background_color)
        self.player = Player(*get_player())
        self.stats_display = TextDisplay("", (0, 255, 0), background_color, (10, 10))
        self.smithing_table = Interactable(
            (100, 100, 100, 100),
            (255, 0, 0),
            self.player,
            lambda x: SCENEMANAGER.switch_scene(1),
        )

        self.on_enter()

    def on_enter(self):
        self.stats_display.set_display(None)

    def get_objects(self):
        return {
            "player": self.player,
            "stats": self.stats_display,
            "smithing_table": self.smithing_table,
        }

    def get_closest_interactable(self) -> Interactable:
        return self.smithing_table

    def step(self):
        obstacles = [self.smithing_table]
        player_movement_step(obstacles)


class ImageInput(Scene):

    def __init__(self, background_color):
        super().__init__(background_color)

        self.canvas = Canvas()
        self.stats_display = TextDisplay("", (0, 255, 0), background_color, (10, 10))

    def on_enter(self):
        img = Image.open(
            r"D:\DHBW\projekte_semester_6\instance_segmentation\training\data\training_data\v1\3.png"
        )
        self.canvas.load_img(img)
        self.stats_display.set_display(None)

    def get_objects(self):
        return {"canvas": self.canvas, "stats": self.stats_display}

    def step(self):
        return None

    def use_img(self):
        img = self.canvas.store_img()

    def on_exit(self):
        self.use_img()
        SCENEMANAGER.switch_scene(0)


SCENEMANAGER = SceneManager([MainGame((0, 0, 0)), ImageInput((100, 110, 125))])
