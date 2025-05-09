import pygame

PLAYER = pygame.Rect((300,300,50,50))
PLAYER_COLOR = (255,0,0)

def get_player()->tuple[pygame.Rect,tuple]:
    return (PLAYER,PLAYER_COLOR)

def player_movement_step():
    player = PLAYER # define reference in local scope for better performance
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_ip(0,-1) # y: -1 up
    if key[pygame.K_a]:
        player.move_ip(-1,0) # x: -1 left
    if key[pygame.K_s]:
        player.move_ip(0,1) # y: 1 down
    if key[pygame.K_d]:
        player.move_ip(1,0) # x: 1 right