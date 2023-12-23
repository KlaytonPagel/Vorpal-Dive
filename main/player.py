import pygame
import json
import os
from config import *
from projectiles import Projectile
from sprites import Weapon, WeaponAnimation
from HUD import HUD
from inventory import Inventory
from settings_screen import Settings


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
        self.image = pygame.image.load("textures/Player.png").convert_alpha()
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
        self.shooting = False
        self.swinging = False
        self.start_swing = True
        self.weapon_animation = None
        self.swing_direction = 'right'
        self.can_attack = True
        self.attack_cooldown = pygame.time.get_ticks()
        self.player_damage = 10
        self.swing_image_index = 0
        self.attack_speed = 1

        # default player stats
        self.player_speed = 5

        self.paused = False
        self.mobile_mode = False
        self.inventory_opened = False
        self.option_opened = False
        self.settings_opened = False
        self.just_closed_option = False
        self.selected_item = None
        self.inventory = Inventory(self.hud_group)

        self.player_data = {}
        self.load_player_data()
        self.hud_elements = {}
        self.HUD = HUD(self.hud_group, self.hud_elements, self.player_data)
        self.settings_menu = Settings()

        # create the players weapon
        self.current_weapon = self.create_weapon()

    # Load all player stats and variables from JSON file___________________________________________
    def load_player_data(self):
        if not os.path.isfile('json/player_data.json'):
            self.save_player_data()
        with open('json/player_data.json') as player_data_file:
            self.player_data = json.load(player_data_file)
            self.max_health = self.player_data['max_health']
            self.current_health = self.player_data['current_health']
            self.player_speed = self.player_data['player_speed']
            self.player_damage = self.player_data['player_damage']

    # Save all player stats and variables from JSON file___________________________________________
    def save_player_data(self):
        player_data = {'max_health': self.max_health, 'current_health': self.current_health,
                       'player_speed': self.player_speed, 'player_damage': self.player_damage}
        with open('json/player_data.json', 'w') as player_data_file:
            json.dump(player_data, player_data_file)

    # track all user input for the player__________________________________________________________
    def player_input(self, event_list):

        # Keyboard inputs
        keys = pygame.key.get_pressed()

        # movement Keys
        if not self.mobile_mode:
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                # if player presses the inventory button
                if self.hud_elements['inventory_icon'].rect.collidepoint(x, y):
                    if not self.inventory_opened:
                        self.inventory_opened = True
                        self.settings_opened = False
                        self.inventory.update_inventory()
                    else:
                        self.inventory_opened = False

                # if player presses the settings menu button
                if self.hud_elements['setting_icon'].rect.collidepoint(x, y):
                    if not self.settings_opened:
                        self.settings_opened = True
                        self.inventory_opened = False
                    else:
                        self.settings_opened = False

                if self.settings_opened:
                    if self.settings_menu.settings_options['mobile_mode'].rect.collidepoint(x, y):
                        if self.mobile_mode:
                            self.mobile_mode = False
                        else:
                            self.mobile_mode = True


                # if an option window is open
                if self.option_opened:
                    for option in self.hud_group:
                        if option.name == 'equip' or option.name == 'secondary':
                            if option.rect.collidepoint(x, y):
                                self.inventory.swap_items(option, self.selected_item)
                                self.current_weapon.kill()
                                del self.current_weapon
                                self.current_weapon = self.create_weapon()
                            option.kill()
                            del option
                            self.option_opened = False
                            self.just_closed_option = True

                # if player selects an item icon in the inventory
                if self.inventory_opened and not self.option_opened:
                    if not self.just_closed_option:
                        for item in self.inventory.inventory_items:
                            if item.rect.collidepoint(x, y):
                                self.inventory.swap_item_buttons((x, y))
                                self.option_opened = True
                                self.selected_item = item
                    self.just_closed_option = False

                if not self.mobile_mode:
                    if self.current_weapon.weapon_type == 'range':
                        self.shooting = True
                    if self.current_weapon.weapon_type == 'melee':
                        self.set_direction((x, y))
                        self.swinging = True

                if self.mobile_mode:
                    # movement
                    if self.hud_elements['up_arrow'].rect.collidepoint(x, y):
                        self.player_direction.y = -1
                    if self.hud_elements['right_arrow'].rect.collidepoint(x, y):
                        self.player_direction.x = 1
                    if self.hud_elements['down_arrow'].rect.collidepoint(x, y):
                        self.player_direction.y = 1
                    if self.hud_elements['left_arrow'].rect.collidepoint(x, y):
                        self.player_direction.x = -1

                    # attacking
                    if self.hud_elements['up_attack'].rect.collidepoint(x, y):
                        self.swing_direction = 'up'
                        if self.current_weapon.weapon_type == 'melee':
                            self.swinging = True
                        if self.current_weapon.weapon_type == 'range':
                            self.shooting = True
                    if self.hud_elements['right_attack'].rect.collidepoint(x, y):
                        self.swing_direction = 'right'
                        if self.current_weapon.weapon_type == 'melee':
                            self.swinging = True
                        if self.current_weapon.weapon_type == 'range':
                            self.shooting = True
                    if self.hud_elements['down_attack'].rect.collidepoint(x, y):
                        self.swing_direction = 'down'
                        if self.current_weapon.weapon_type == 'melee':
                            self.swinging = True
                        if self.current_weapon.weapon_type == 'range':
                            self.shooting = True
                    if self.hud_elements['left_attack'].rect.collidepoint(x, y):
                        self.swing_direction = 'left'
                        if self.current_weapon.weapon_type == 'melee':
                            self.swinging = True
                        if self.current_weapon.weapon_type == 'range':
                            self.shooting = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.shooting = False
                if self.mobile_mode:
                    self.player_direction = pygame.math.Vector2(0, 0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.swap_weapon()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                if self.inventory_opened:
                    self.inventory_opened = False
                else:
                    self.inventory.update_inventory()
                    self.inventory_opened = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.save_player_data()
                self.inventory.save_inventory()

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

        # update all projectile and weapon animations
        self.update_weapon_effects()

        if self.current_weapon.weapon_type == 'range':
            self.shoot()

        if self.current_weapon.weapon_type == 'melee':
            self.swing()

        # update the current weapons position to match the player
        self.update_weapon()
        self.HUD.update_hud()

        if self.inventory_opened:
            self.inventory.display_inventory()

        if self.settings_opened:
            self.settings_menu.update_settings_menu(self.mobile_mode)

    # create the players weapon____________________________________________________________________
    def create_weapon(self):
        weapon_id = self.inventory.inventory_slots['equipped'][1]
        weapon = self.inventory.item_IDs[weapon_id]
        self.adjust_damage(weapon[2])
        self.attack_speed = weapon[3]
        return Weapon(self.rect.midright, weapon[0], (self.visible_group, self.weapon_group),
                      (tile_size, tile_size), weapon[2], weapon[1])

    # Swap the players main weapon with their secondary weapon____________________________________
    def swap_weapon(self):
        equipped_weapon_id = self.inventory.inventory_slots['equipped'][1]
        secondary_weapon_id = self.inventory.inventory_slots['secondary'][1]
        self.inventory.inventory_slots['equipped'][1] = secondary_weapon_id
        self.inventory.inventory_slots['secondary'][1] = equipped_weapon_id
        self.current_weapon.kill()
        del self.current_weapon
        self.current_weapon = self.create_weapon()
        if self.inventory_opened:
            self.inventory.update_inventory()

    # update the players weapon position___________________________________________________________
    def update_weapon(self):
        self.current_weapon.rect.midleft = (self.rect.midright[0] - 5, self.rect.midright[1])

    # set the players attacking direction__________________________________________________________
    def set_direction(self, mouse_pos):
        screen = pygame.display.get_surface()
        mouse_pos = pygame.math.Vector2(mouse_pos)
        center_pos = pygame.math.Vector2(screen.get_width() // 2, screen.get_height() // 2)
        direction = (mouse_pos - center_pos).normalize()
        direction.x, direction.y = int(round(direction.x)), int(round(direction.y))
        if direction.x == 1 and direction.y == 0:
            self.swing_direction = 'right'
        if direction.x == 1 and direction.y == -1:
            self.swing_direction = 'right'
        if direction.x == 0 and direction.y == 1:
            self.swing_direction = 'down'
        if direction.x == 1 and direction.y == 1:
            self.swing_direction = 'down'
        if direction.x == -1 and direction.y == 0:
            self.swing_direction = 'left'
        if direction.x == -1 and direction.y == 1:
            self.swing_direction = 'left'
        if direction.x == 0 and direction.y == -1:
            self.swing_direction = 'up'
        if direction.x == -1 and direction.y == -1:
            self.swing_direction = 'up'

    # if you are attacking with a ranged weapon shoot______________________________________________
    def shoot(self):
        screen = pygame.display.get_surface()
        if self.shooting and self.can_attack:
            if self.mobile_mode:
                if self.swing_direction == 'right':
                    end_point = pygame.math.Vector2(screen.get_width() // 2 + 10, screen.get_height() // 2)
                elif self.swing_direction == 'down':
                    end_point = pygame.math.Vector2(screen.get_width() // 2, screen.get_height() // 2 + 10)
                elif self.swing_direction == 'left':
                    end_point = pygame.math.Vector2(screen.get_width() // 2 - 10, screen.get_height() // 2)
                else:
                    end_point = pygame.math.Vector2(screen.get_width() // 2, screen.get_height() // 2 - 10)
            else:
                end_point = pygame.math.Vector2(pygame.mouse.get_pos())
            starting_point = pygame.math.Vector2(screen.get_width() // 2, screen.get_height() // 2)

            Projectile((self.visible_group, self.weapon_group), self.rect.center,
                       starting_point, end_point, self.obstacle_group, self.player_damage)

            self.can_attack = False
            self.attack_cooldown = pygame.time.get_ticks()

    # if you are attacking with a melee weapon then swing__________________________________________
    def swing(self):
        if self.swinging and self.can_attack:
            swing_animation_frames = [pygame.image.load('textures/32X32/HUD/slash_first.png').convert_alpha(),
                                      pygame.image.load('textures/32X32/HUD/slash_second.png').convert_alpha()]

            if self.start_swing:
                self.weapon_animation = WeaponAnimation((self.rect.topright[0] + 16, self.rect.topright[1] - 16),
                                                        swing_animation_frames[0],
                                                        (self.visible_group, self.weapon_group),
                                                        self.player_damage, 'animation')
                self.start_swing = False

            if self.swing_direction == 'right':
                self.weapon_animation.image = swing_animation_frames[int(self.swing_image_index)]
                self.weapon_animation.rect.topleft = (self.rect.topright[0] + 16, self.rect.topright[1] - 16)
            elif self.swing_direction == 'down':
                self.weapon_animation.image = swing_animation_frames[int(self.swing_image_index)]
                self.weapon_animation.image = pygame.transform.rotate(self.weapon_animation.image, 270)
                self.weapon_animation.rect.topleft = (self.rect.bottomleft[0] - 16, self.rect.bottomleft[1] + 16)
            elif self.swing_direction == 'left':
                self.weapon_animation.image = swing_animation_frames[int(self.swing_image_index)]
                self.weapon_animation.image = pygame.transform.rotate(self.weapon_animation.image, 180)
                self.weapon_animation.rect.topleft = (self.rect.topleft[0] - 32, self.rect.topleft[1] - 16)
            else:
                self.weapon_animation.image = swing_animation_frames[int(self.swing_image_index)]
                self.weapon_animation.image = pygame.transform.rotate(self.weapon_animation.image, 90)
                self.weapon_animation.rect.topleft = (self.rect.topleft[0] - 16, self.rect.topleft[1] - 32)

            self.swing_image_index += 0.35
            if self.swing_image_index >= len(swing_animation_frames):
                self.swing_image_index = 0
                self.swinging = False
                for effect in self.weapon_group:
                    if effect.weapon_type == 'animation':
                        effect.kill()
                        del effect

                self.can_attack = False
                self.start_swing = True
                self.attack_cooldown = pygame.time.get_ticks()

    # update all weapon projectiles and animations_________________________________________________
    def update_weapon_effects(self):
        for effect in self.weapon_group:
            if effect.weapon_type == 'projectile':
                effect.update()

    # all player cool downs________________________________________________________________________
    def cool_downs(self):
        current_time = pygame.time.get_ticks()

        # Shooting cooldown
        if not self.can_attack:
            if current_time - self.attack_cooldown > 1000 // self.attack_speed:
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
                        if sprite.enemy_direction.x != 0:
                            self.rect.x += sprite.enemy_direction.x * 15
                            self.check_obstacle_collisions('horizontal')
                        if sprite.enemy_direction.y != 0:
                            self.rect.y += sprite.enemy_direction.y * 15
                            self.check_obstacle_collisions('vertical')
                        self.invincible = True
                        self.invincibility_cooldown = 0
