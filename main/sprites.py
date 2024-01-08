import pygame
from config import *


# A Class to create the sprites for each object and tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, side='default', name='default', sprite_size=(tile_size, tile_size)):
        super().__init__(group)
        self.image = surf
        self.image = pygame.transform.scale(self.image, sprite_size)
        if side == 'top right' or side == 'bottom left inside':
            self.rect = self.image.get_rect(bottomleft=pos)
        elif side == 'top left' or side == 'bottom right inside':
            self.rect = self.image.get_rect(bottomright=pos)
        elif side == 'bottom right' or side == 'top left inside':
            self.rect = self.image.get_rect(topleft=pos)
        elif side == 'bottom left' or side == 'top right inside':
            self.rect = self.image.get_rect(topright=pos)
        elif side == 'bottom':
            self.rect = self.image.get_rect(midtop=pos)
        elif side == 'top':
            self.rect = self.image.get_rect(midbottom=pos)
        elif side == 'right':
            self.rect = self.image.get_rect(midleft=pos)
        elif side == 'left':
            self.rect = self.image.get_rect(midright=pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.rect = self.rect.inflate(0, -10)
        self.name = name


class HUDobject(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, name='default', slot='default'):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.name = name
        self.slot = slot


class Text(pygame.sprite.Sprite):
    def __init__(self, pos, words, group, size, color, name='default'):
        super().__init__(group)
        self.image = pygame.font.Font(None, size)
        self.image = self.image.render(str(words), True, color)
        self.rect = self.image.get_rect(center=pos)
        self.name = name


class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos, image, group, sprite_size, damage,  weapon_type='default', name='default'):
        super().__init__(group)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, sprite_size)
        self.rect = self.image.get_rect(center=pos)
        self.damage = damage
        self.name = name
        self.weapon_type = weapon_type


class WeaponAnimation(pygame.sprite.Sprite):
    def __init__(self, pos, image, group, damage,  weapon_type='default', name='default'):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.damage = damage
        self.name = name
        self.weapon_type = weapon_type
