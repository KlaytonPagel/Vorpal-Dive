import pygame
from config import *


# class to create enemy sprites____________________________________________________________________
class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, position, grid, obstacle_group, weapon_group):
        super().__init__(group)

        # Enemy sprite setup
        self.image = pygame.image.load("textures/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.rect = self.rect.inflate(0, -10)
        self.enemy_direction = pygame.math.Vector2()

        # grid tile location set up
        self.grid = grid
        self.near_tile_objects = []
        self.current_tile = (0, 1)

        # invincibility frames
        self.invincible = False
        self.invincible_cool_down = pygame.time.get_ticks()

        # enemy health setup
        self.current_health = 20

        # position set up
        self.starting_position = pygame.math.Vector2(position)
        self.position_x, self.position_y = position[0] + tile_size // 2, position[1] + tile_size // 2

        # declaring sprite groups
        self.obstacle_group = obstacle_group
        self.weapon_group = weapon_group

    # update the enemy every frame_________________________________________________________________
    def update(self, player_position, delta_time):
        self.enemy_pathfinding(player_position, delta_time)
        self.check_weapon_collision()
        self.cool_downs()

    # enemy cool downs____________________________________________________________________________
    def cool_downs(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.invincible_cool_down >= 300:
            self.invincible = False

    # set the enemies current grid tile____________________________________________________________
    def get_current_tile(self):
        self.current_tile = self.grid.get_grid_tile(self.rect.topleft)

    # gets the tiles close to the enemy____________________________________________________________
    def get_near_tiles(self):
        self.near_tile_objects.clear()
        for x in range(-1, 2):
            for y in range(-1, 2):
                try:
                    for wall in self.grid.grid[(self.current_tile[0] + x, self.current_tile[1] + y)]:
                        self.near_tile_objects.append(wall)
                except: pass

    # move towards the player if within range______________________________________________________
    def enemy_pathfinding(self, player_position, delta_time):
        # normalize the direction vector so the length of the line doesn't affect enemy speed
        if (abs(player_position[0] - self.position_x) <= enemy_agro_range * tile_size and
                abs(player_position[1] - self.position_y) <= enemy_agro_range * tile_size):
            try:
                self.enemy_direction = (pygame.math.Vector2(player_position) -
                                        pygame.math.Vector2(self.position_x, self.position_y)).normalize()
            except:
                pass

            # update the floating point variables
            self.position_x += self.enemy_direction.x * enemy_speed * delta_time
            self.rect.centerx = round(self.position_x)
            self.check_obstacle_collisions('horizontal')
            self.position_y += self.enemy_direction.y * enemy_speed * delta_time
            self.rect.centery = round(self.position_y)
            self.check_obstacle_collisions('vertical')
            self.rect.center = (self.position_x, self.position_y)

            self.get_current_tile()

    # adjust the enemies health____________________________________________________________________
    def adjust_current_health(self, amount):
        self.current_health += amount
        if self.current_health <= 0:
            self.kill()

    # check for collision between enemy and obstacle_______________________________________________
    def check_obstacle_collisions(self, direction):
        if collision:
            self.get_near_tiles()

            # Check obstacle collision
            for sprite in self.near_tile_objects:
                if direction == 'horizontal':
                    if self.rect.colliderect(sprite) and self.enemy_direction.x > 0:
                        self.rect.right = sprite.rect.left
                        self.position_x, self.position_y = self.rect.center
                    elif self.rect.colliderect(sprite) and self.enemy_direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.position_x, self.position_y = self.rect.center
                if direction == 'vertical':
                    if self.rect.colliderect(sprite) and self.enemy_direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.position_x, self.position_y = self.rect.center
                    elif self.rect.colliderect(sprite) and self.enemy_direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.position_x, self.position_y = self.rect.center

    # check for collision between enemy and a projectile___________________________________________
    def check_weapon_collision(self):
        if collision:

            # check projectile collision
            for sprite in self.weapon_group.sprites():
                if self.rect.colliderect(sprite) and not self.invincible:
                    if sprite.weapon_type != 'melee' and sprite.weapon_type != 'range':
                        if sprite.weapon_type == 'projectile':
                            sprite.kill()
                        if sprite.weapon_type == 'animation':
                            self.invincible = True
                            self.invincible_cool_down = pygame.time.get_ticks()
                        self.adjust_current_health(-sprite.damage)
                        self.enemy_direction = -self.enemy_direction
                        if self.enemy_direction.x != 0:
                            self.rect.x += self.enemy_direction.x * tile_size/2
                            self.check_obstacle_collisions('horizontal')
                        if self.enemy_direction.y != 0:
                            self.rect.y += self.enemy_direction.y * tile_size/2
                            self.check_obstacle_collisions('vertical')
                        self.position_x, self.position_y = self.rect.center
