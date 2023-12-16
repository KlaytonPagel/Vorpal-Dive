import pygame
from config import *


# A class to create and manage the player character
class Player(pygame.sprite.Sprite):
    def __init__(self, group, position, obstacle_group):
        super().__init__(group)

        # General sprite setup
        self.image = pygame.image.load("../textures/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.rect = self.rect.inflate(0, -20)
        self.direction = pygame.math.Vector2()

        self.obstacle_group = obstacle_group

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
        self.check_collisions()

    def check_collisions(self):
        tolerance = 10
        if collision:

            # Check obstacle collision
            for sprite in self.obstacle_group.sprites():
                if self.rect.colliderect(sprite) and abs(self.rect.right - sprite.rect.left) <= tolerance:
                    self.rect.right = sprite.rect.left
                elif self.rect.colliderect(sprite) and abs(self.rect.left - sprite.rect.right) <= tolerance:
                    self.rect.left = sprite.rect.right
                elif self.rect.colliderect(sprite) and abs(self.rect.top - sprite.rect.bottom) <= tolerance:
                    self.rect.top = sprite.rect.bottom
                elif self.rect.colliderect(sprite) and abs(self.rect.bottom - sprite.rect.top) <= tolerance:
                    self.rect.bottom = sprite.rect.top
