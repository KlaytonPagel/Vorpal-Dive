import pygame
from config import *


# class for all game projectiles___________________________________________________________________
class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, position, starting_point, end_point,
                 obstacle_group, damage, player_speed, player_direction):
        super().__init__(group)

        # Projectile sprite setup
        self.image = pygame.image.load('textures/32X32/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size // 4, tile_size // 4))
        self.rect = self.image.get_rect(center=position)
        self.weapon_type = 'projectile'

        # points to find the direction to shoot in
        self.starting_point = pygame.math.Vector2(starting_point)
        self.end_point = pygame.math.Vector2(end_point)
        self.projectile_speed = projectile_speed

        # normalize the direction vector so the length of the line doesn't affect projectile speed
        self.projectile_direction = (self.end_point - self.starting_point).normalize()

        # use separate points to determine the projectile position, this allows use of floating numbers for precision
        self.position_x, self.position_y = position

        # Groups to check collisions with
        self.obstacle_group = obstacle_group

        # distance the projectile has traveled
        self.projectile_distance = 0

        # projectiles damage
        self.damage = damage

        # players speed and direction to add to the projectile
        self.player_speed = player_speed
        self.player_direction = player_direction
        self.player_adjustment_x = self.player_direction.x * self.player_speed * .3
        self.player_adjustment_y = self.player_direction.y * self.player_speed * .3
        if self.player_adjustment_x == 0:
            self.player_adjustment_x = 1
        if self.player_adjustment_y == 0:
            self.player_adjustment_y = 1

    # update the projectiles position______________________________________________________________
    def update(self, delta_time):

        # update the floating point variables
        if ((self.player_adjustment_x > 1 and self.projectile_direction.x > 0) or
                (self.player_adjustment_x < 0 and self.projectile_direction.x < 0)):
            self.position_x += self.projectile_direction.x * self.projectile_speed * delta_time * abs(self.player_adjustment_x)
        else:
            self.position_x += self.projectile_direction.x * self.projectile_speed * delta_time

        if ((self.player_adjustment_y > 1 and self.projectile_direction.y > 0) or
                (self.player_adjustment_y < 0 and self.projectile_direction.y < 0)):
            self.position_y += self.projectile_direction.y * self.projectile_speed * delta_time * abs(self.player_adjustment_y)
        else:
            self.position_y += self.projectile_direction.y * self.projectile_speed * delta_time
        self.rect.center = (self.position_x, self.position_y)

        # update to projectiles traveled distance
        self.projectile_distance += self.projectile_speed * delta_time

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
        if self.projectile_distance > (projectile_range * tile_size):
            self.kill()
