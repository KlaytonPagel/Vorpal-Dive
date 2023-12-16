import pygame
from config import *
from dungeon_generator import Dungeon

# start pygame_____________________________________________________________________________________
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('py dungeon')
running = True

# Declare groups___________________________________________________________________________________
visible_group = pygame.sprite.Group()

# create objects___________________________________________________________________________________
Dungeon(visible_group)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    visible_group.draw(screen)

    pygame.display.flip()
