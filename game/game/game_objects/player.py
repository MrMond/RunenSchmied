import pygame
from configparser import ConfigParser as CP
import os
import ast

config = CP()
config.read(os.path.join(os.getcwd(), "etc", ".conf"))

SCREEN_SIZE = ast.literal_eval(config.get("game", "screen_size"))

PLAYER = pygame.Rect((300, 300, 50, 50))
PLAYER_COLOR = (255, 255, 255)
SPEED = ast.literal_eval(config.get("game", "player_speed"))

class dt:
    def __init__(self):
        self.tick = pygame.time.get_ticks()
    
    def get_dt(self):
        '''returns the amount of ticks between two calls of this function'''
        dt = (pygame.time.get_ticks()-self.tick)
        self.tick = pygame.time.get_ticks()
        return dt

DT = dt()

def get_player() -> tuple[pygame.Rect, tuple]:
    return (PLAYER, PLAYER_COLOR)


def player_movement_step(obstacles: list[pygame.Rect]):
    player = PLAYER  # define reference in local scope for better performance

    # smooth out movement
    dt = DT.get_dt()

    # perform movement
    direction = [0, 0]
    player_position = player.x, player.y

    key = pygame.key.get_pressed()
    if key[pygame.K_w] or key[pygame.K_UP]:
        direction[1] -= SPEED * dt  # y: -1 up
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        direction[0] -= SPEED * dt  # x: -1 left
    if key[pygame.K_s] or key[pygame.K_DOWN]:
        direction[1] += SPEED * dt  # y: 1 down
    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        direction[0] += SPEED * dt  # x: 1 right

    player.move_ip(*direction)

    # check collisions 1) with window, 2) with other objects
    player.clamp_ip(pygame.display.get_surface().get_rect())

    if player.collidelist(obstacles) >= 0:
        # resetting the position upon collsion gets buggy at low framerates (because of dt in movement), but this is just a POC, so I won't fix
        player.x, player.y = player_position 
