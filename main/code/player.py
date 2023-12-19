import pygame
from config import *
from projectiles import Projectile
from sprites import HUD


# A class to create and manage the player character________________________________________________
class Player(pygame.sprite.Sprite):
    def __init__(self, group, position, screen, visible_group, obstacle_group, projectile_group, enemy_group, hud_group):
        super().__init__(group)

        self.screen = screen

        # Player sprite setup
        self.image = pygame.image.load("../textures/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.rect = self.rect.inflate(0, -10)
        self.position = position
        self.player_direction = pygame.math.Vector2()

        # health stuff
        self.max_health = max_health
        self.max_health_bar = None
        self.current_health = max_health
        self.current_health_bar = None
        self.invincibility_cooldown = fps // 2
        self.invincible = False

        # Projectile Stuff
        self.shooting = False
        self.can_shoot = True
        self.shoot_cooldown = fps

        # Define sprite groups
        self.obstacle_group = obstacle_group
        self.visible_group = visible_group
        self.projectile_group = projectile_group
        self.enemy_group = enemy_group
        self.hud_group = hud_group

        self.health_bars()

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

        if keys[pygame.K_EQUALS]:
            self.adjust_current_health(10)

        if keys[pygame.K_MINUS]:
            self.adjust_current_health(-10)

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

        # Move the player
        self.player_input(event_list)
        if self.player_direction.magnitude() != 0:
            self.player_direction = self.player_direction.normalize()

        if self.player_direction.x != 0:
            self.rect.x += self.player_direction.x * player_speed
            self.check_obstacle_collisions('horizontal')
        if self.player_direction.y != 0:
            self.rect.y += self.player_direction.y * player_speed
            self.check_obstacle_collisions('vertical')

        self.check_enemy_collision()
        self.cool_downs()
        self.shoot()

        # update all visible projectiles
        for projectile in self.projectile_group:
            projectile.update()

    # all player cool downs________________________________________________________________________
    def cool_downs(self):

        # Shooting cooldown
        if not self.can_shoot:
            self.shoot_cooldown += projectile_fire_rate
            if self.shoot_cooldown >= fps:
                self.can_shoot = True

    # if you are shooting then shoot_______________________________________________________________
    def shoot(self):
        if self.shooting and self.can_shoot:
            starting_point = pygame.math.Vector2(screen_width // 2, screen_height // 2)
            end_point = pygame.math.Vector2(pygame.mouse.get_pos())

            Projectile((self.visible_group, self.projectile_group), self.rect.center,
                       starting_point, end_point, self.obstacle_group, self.enemy_group)

            self.can_shoot = False
            self.shoot_cooldown = 0

    # Set up the players initial health bars_______________________________________________________
    def health_bars(self):
        # health bar for maximum amount of health
        max_health_bar_surface = pygame.Surface((self.max_health, 10))
        max_health_bar_surface.fill((255, 255, 255))
        self.max_health_bar = HUD((20, 20), max_health_bar_surface, self.hud_group, 'max_health_bar')

        # health bar for players current health
        current_health_bar_surface = pygame.Surface((self.current_health, 10))
        current_health_bar_surface.fill((255, 0, 0))
        self.current_health_bar = HUD((20, 20), current_health_bar_surface, self.hud_group, 'current_health_bar')

    # adjust the players maximum health____________________________________________________________
    def adjust_max_health(self, amount):
        self.max_health += amount
        if self.max_health < 0:
            self.max_health = 0
        max_health_bar_surface = pygame.Surface((self.max_health, 10))
        max_health_bar_surface.fill((255, 255, 255))
        self.max_health_bar.image = max_health_bar_surface

    # adjust players current health________________________________________________________________
    def adjust_current_health(self, amount):
        self.current_health += amount
        if self.current_health < 0:
            self.current_health = 0
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        current_health_bar_surface = pygame.Surface((self.current_health, 10))
        current_health_bar_surface.fill((255, 0, 0))
        self.current_health_bar.image = current_health_bar_surface

    # Check for any collisions between the player and obstacles____________________________________
    def check_obstacle_collisions(self, direction):
        if collision:

            # Check obstacle collision
            for sprite in self.obstacle_group.sprites():
                if direction == 'horizontal':
                    if self.rect.colliderect(sprite) and self.player_direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.rect.colliderect(sprite) and self.player_direction.x < 0:
                        self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.rect.colliderect(sprite) and self.player_direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.rect.colliderect(sprite) and self.player_direction.y > 0:
                        self.rect.bottom = sprite.rect.top

    # check for any collisions between the player and enemies______________________________________
    def check_enemy_collision(self):
        if collision:

            if self.invincible:
                self.invincibility_cooldown += 1
                if self.invincibility_cooldown >= fps // 2:
                    self.invincible = False

            else:
                # check enemy collision
                for sprite in self.enemy_group.sprites():
                    if self.rect.colliderect(sprite):
                        self.adjust_current_health(-10)
                        self.player_direction = sprite.enemy_direction
                        if sprite.enemy_direction.x != 0:
                            self.rect.x += self.player_direction.x * 15
                            self.check_obstacle_collisions('horizontal')
                        if self.player_direction.y != 0:
                            self.rect.y += self.player_direction.y * 15
                            self.check_obstacle_collisions('vertical')
                        self.invincible = True
                        self.invincibility_cooldown = 0


