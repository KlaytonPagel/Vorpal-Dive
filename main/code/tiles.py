import pygame
from config import *


# A Class to create the sprites for each object and tile
class Visible(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, name='default'):
        super().__init__(group)
        self.image = pygame.image.load(surf).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)
        self.rect = self.rect.inflate(0, -15)
        self.name = name
