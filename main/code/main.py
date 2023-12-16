import pygame
from config import *
from dungeon_generator import Dungeon
from player import Player

# start pygame_____________________________________________________________________________________
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('py dungeon')
running = True

# Declare groups___________________________________________________________________________________
visible_group = pygame.sprite.Group()

# create objects___________________________________________________________________________________
dungeon = Dungeon(visible_group)
player = Player(visible_group, dungeon.player_start_position)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    visible_group.draw(screen)
    player.update()

    pygame.display.flip()
