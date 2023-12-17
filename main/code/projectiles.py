import pygame
from config import *


# class for all game projectiles___________________________________________________________________
class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, position, starting_point, end_point, obstacle_group):
        super().__init__(group)

        # Projectile sprite setup
        self.image = pygame.image.load('../textures/32X32/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size // 4, tile_size // 4))
        self.rect = self.image.get_rect(center=position)
        self.projectile_direction = pygame.math.Vector2()

        # points to find the direction to shoot in
        self.starting_point = pygame.math.Vector2(starting_point)
        self.end_point = pygame.math.Vector2(end_point)

        # use separate points to determine the projectile position, this allows use of floating numbers for precision
        self.position_x, self.position_y = position

        # Groups to check collisions with
        self.obstacle_group = obstacle_group

        # distance the projectile has traveled
        self.projectile_distance = 0

    # update the projectiles position______________________________________________________________
    def update(self):
        # normalize the direction vector so the length of the line doesn't affect projectile speed
        self.projectile_direction = (self.end_point - self.starting_point).normalize()

        # update the floating point variables
        self.position_x += self.projectile_direction.x * projectile_speed
        self.position_y += self.projectile_direction.y * projectile_speed
        self.rect.center = (self.position_x, self.position_y)

        # update to projectiles traveled distance
        self.projectile_distance += projectile_speed

        self.check_collisions()
        self.check_distance()

    # check for collisions between the projectile and other sprites________________________________
    def check_collisions(self):
        if collision:

            # Check obstacle collision
            for sprite in self.obstacle_group.sprites():
                if self.rect.colliderect(sprite):
                    self.kill()

    # check if the distance the projectile has traveled exceeds the range__________________________
    def check_distance(self):
        if self.projectile_distance > projectile_range * tile_size:
            self.kill()
