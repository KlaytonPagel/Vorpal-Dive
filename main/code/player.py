import pygame
from config import *


# A class to create and manage the player character
class Player(pygame.sprite.Sprite):
    def __init__(self, group, position):
        super().__init__(group)

        # General sprite setup
        self.image = pygame.image.load("../textures/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.rect = self.rect.inflate(0, -20)
        self.direction = pygame.math.Vector2()

    # track all user input for the player
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    # Update all player function
    def update(self):
        self.player_input()
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * player_speed
