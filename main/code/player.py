import math

import pygame
from config import *
from projectiles import Projectile


# A class to create and manage the player character________________________________________________
class Player(pygame.sprite.Sprite):
    def __init__(self, group, position, visible_group, obstacle_group, projectile_group):
        super().__init__(group)

        # Player sprite setup
        self.image = pygame.image.load("../textures/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.rect = self.rect.inflate(0, -10)
        self.player_direction = pygame.math.Vector2()

        # Projectile Stuff
        self.shooting = False

        # Define sprite groups
        self.obstacle_group = obstacle_group
        self.visible_group = visible_group
        self.projectile_group = projectile_group

    # track all user input for the player__________________________________________________________
    def player_input(self, event_list):

        # Keyboard inputs
        keys = pygame.key.get_pressed()

        # movement Keys
        if keys[pygame.K_w]:
            self.player_direction.y = -1
        elif keys[pygame.K_s]:
            self.player_direction.y = 1
        else:
            self.player_direction.y = 0
        if keys[pygame.K_d]:
            self.player_direction.x = 1
        elif keys[pygame.K_a]:
            self.player_direction.x = -1
        else:
            self.player_direction.x = 0

        # mouse inputs
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.shooting = False

    # Update all player function___________________________________________________________________
    def update(self, event_list):
        self.player_input(event_list)
        if self.player_direction.magnitude() != 0:
            self.player_direction = self.player_direction.normalize()
        self.rect.center += self.player_direction * player_speed
        self.check_collisions()
        if self.shooting:
            self.shoot()

        # update all visible projectiles
        for projectile in self.projectile_group:
            projectile.update()

    # if you are shooting then shoot______________________________________________________________
    def shoot(self):
        starting_point = pygame.math.Vector2(screen_width // 2, screen_height // 2)
        end_point = pygame.math.Vector2(pygame.mouse.get_pos())

        Projectile((self.visible_group, self.projectile_group), self.rect.center,
                   starting_point, end_point, self.obstacle_group)

    # Check for any collisions with the player_____________________________________________________
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
