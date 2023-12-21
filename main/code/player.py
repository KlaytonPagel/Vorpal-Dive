import pygame, json, os
from config import *
from projectiles import Projectile
from sprites import Weapon
from HUD import HUD
from inventory import Inventory


# A class to create and manage the player character________________________________________________
class Player(pygame.sprite.Sprite):
    def __init__(self, group, position, visible_group, obstacle_group, weapon_group, enemy_group, hud_group):
        super().__init__(group)

        # Define sprite groups
        self.obstacle_group = obstacle_group
        self.visible_group = visible_group
        self.weapon_group = weapon_group
        self.enemy_group = enemy_group
        self.hud_group = hud_group

        # Player sprite setup
        self.image = pygame.image.load("../textures/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=position)
        self.rect = self.rect.inflate(0, -10)
        self.position = position
        self.player_direction = pygame.math.Vector2()

        # default health values
        self.max_health = 100
        self.current_health = 100
        self.invincibility_cooldown = fps // 2
        self.invincible = False

        # Default attacking values
        self.attacking = False
        self.can_attack = True
        self.attack_cooldown = pygame.time.get_ticks()
        self.player_damage = 10

        # default player stats
        self.player_speed = 5

        self.paused = False
        self.inventory_opened = False
        self.inventory = Inventory()

        self.player_data = {}
        self.load_player_data()
        self.hud_elements = {}
        self.HUD = HUD(self.hud_group, self.hud_elements, self.player_data)

        # create the players weapon
        self.current_weapon = self.create_weapon()

    # Load all player stats and variables from JSON file___________________________________________
    def load_player_data(self):
        if not os.path.isfile('../json/player_data.json'):
            self.save_player_data()
        with open('../json/player_data.json') as player_data_file:
            self.player_data = json.load(player_data_file)
            self.max_health = self.player_data['max_health']
            self.current_health = self.player_data['current_health']
            self.player_speed = self.player_data['player_speed']
            self.player_damage = self.player_data['player_damage']

    # Save all player stats and variables from JSON file___________________________________________
    def save_player_data(self):
        player_data = {'max_health': self.max_health, 'current_health': self.current_health,
                       'player_speed': self.player_speed, 'player_damage': self.player_damage}
        with open('../json/player_data.json', 'w') as player_data_file:
            json.dump(player_data, player_data_file)

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
            self.inventory_opened = True

        if keys[pygame.K_MINUS]:
            self.inventory_opened = False

        # mouse inputs
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if self.hud_elements['inventory_icon'].rect.collidepoint(x, y):
                        if not self.inventory_opened:
                            self.inventory_opened = True
                            self.inventory.load_inventory()
                        else:
                            self.inventory_opened = False
                    self.attacking = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.attacking = False

    # Update all player function___________________________________________________________________
    def update(self, event_list):

        # Move the player
        self.player_input(event_list)
        if self.player_direction.magnitude() != 0:
            self.player_direction = self.player_direction.normalize()

        if self.player_direction.x != 0:
            self.rect.x += self.player_direction.x * self.player_speed
            self.check_obstacle_collisions('horizontal')
        if self.player_direction.y != 0:
            self.rect.y += self.player_direction.y * self.player_speed
            self.check_obstacle_collisions('vertical')

        self.check_enemy_collision()
        self.cool_downs()

        if self.current_weapon.weapon_type == 'range':
            self.shoot()

        if self.current_weapon.weapon_type == 'melee':
            pass

        # update all visible projectiles
        for projectile in self.weapon_group:
            projectile.update()

        # update the current weapons position to match the player
        self.update_weapon()
        self.HUD.update_hud()

        if self.inventory_opened:
            self.inventory.update_inventory()

    # create the players weapon____________________________________________________________________
    def create_weapon(self):
        weapon_id = self.inventory.inventory_slots['equipped']
        weapon = self.inventory.item_IDs[weapon_id[2]]
        self.adjust_damage(weapon[2])
        return Weapon(self.rect.midright, weapon[0], (self.visible_group, self.weapon_group),
                      (tile_size, tile_size), weapon[2], weapon[1])

    # update the players weapon position___________________________________________________________
    def update_weapon(self):
        self.current_weapon.rect.midleft = (self.rect.midright[0] - 5, self.rect.midright[1])

    # if you are shooting then shoot_______________________________________________________________
    def shoot(self):
        screen = pygame.display.get_surface()
        if self.attacking and self.can_attack:
            starting_point = pygame.math.Vector2(screen.get_width() // 2, screen.get_height() // 2)
            end_point = pygame.math.Vector2(pygame.mouse.get_pos())

            Projectile((self.visible_group, self.weapon_group), self.rect.center,
                       starting_point, end_point, self.obstacle_group, self.player_damage)

            self.can_attack = False
            self.attack_cooldown = pygame.time.get_ticks()

    # all player cool downs________________________________________________________________________
    def cool_downs(self):
        current_time = pygame.time.get_ticks()

        # Shooting cooldown
        if not self.can_attack:
            if current_time - self.attack_cooldown > 1000 // projectile_fire_rate:
                self.can_attack = True

    # adjust the players maximum health____________________________________________________________
    def adjust_max_health(self, amount):
        self.max_health += amount
        if self.max_health < 0:
            self.max_health = 0
        max_health_bar_surface = pygame.Surface((self.max_health, 10))
        max_health_bar_surface.fill((255, 255, 255))
        self.hud_elements['max_health_bar'].image = max_health_bar_surface

    # adjust players current health________________________________________________________________
    def adjust_current_health(self, amount):
        self.current_health += amount
        if self.current_health < 0:
            self.current_health = 0
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        current_health_bar_surface = pygame.Surface((self.current_health, 10))
        current_health_bar_surface.fill((255, 0, 0))
        self.hud_elements['current_health_bar'].image = current_health_bar_surface

    # adjust the players damage stat_______________________________________________________________
    def adjust_damage(self, amount, adding=False):
        if adding:
            self.player_damage += amount
        self.player_damage = amount
        for sprite in self.hud_group.sprites():
            if sprite.name == 'damage_stat':
                sprite.image = pygame.font.Font(None, 30).render(str(self.player_damage), True, (255, 255, 255))

    # adjust the players movement speed by a defined amount________________________________________
    def adjust_movement_speed(self, amount):
        self.player_speed += amount
        for sprite in self.hud_group.sprites():
            if sprite.name == 'movement_speed_stat':
                sprite.image = pygame.font.Font(None, 30).render(str(self.player_speed), True, (255, 255, 255))

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
