import pygame
from config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, position, obstacle_group):
        super().__init__(group)

        # Enemy sprite setup
        self.image = pygame.image.load("../textures/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.rect = self.rect.inflate(0, -10)
        self.enemy_direction = pygame.math.Vector2()

        self.starting_position = pygame.math.Vector2(position)
        self.position_x, self.position_y = position

        self.obstacle_group = obstacle_group

    def update(self, player_position):
        self.enemy_pathfinding(player_position)

    def enemy_pathfinding(self, player_position):
        # normalize the direction vector so the length of the line doesn't affect enemy speed
        if (abs(player_position[0] - self.position_x) <= enemy_agro_range * tile_size and
                abs(player_position[1] - self.position_y) <= enemy_agro_range * tile_size):
            try:
                self.enemy_direction = (pygame.math.Vector2(player_position) -
                                        pygame.math.Vector2(self.position_x, self.position_y)).normalize()
            except:
                pass

            # update the floating point variables
            self.rect.x += self.enemy_direction.x * enemy_speed
            self.check_collisions('horizontal')
            self.rect.y += self.enemy_direction.y * enemy_speed
            self.check_collisions('vertical')
            self.rect.center = (self.position_x, self.position_y)

    def check_collisions(self, direction):
        if collision:

            # Check obstacle collision
            for sprite in self.obstacle_group.sprites():
                if direction == 'horizontal':
                    if self.rect.colliderect(sprite) and self.enemy_direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.rect.colliderect(sprite) and self.enemy_direction.x < 0:
                        self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.rect.colliderect(sprite) and self.enemy_direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.rect.colliderect(sprite) and self.enemy_direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                self.position_x, self.position_y = self.rect.center
