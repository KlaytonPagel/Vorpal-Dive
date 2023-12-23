import pygame
from sprites import HUDobject, Text


class HUD:
    def __init__(self, hud_group, hud_elements, player_data):
        # Define groups
        self.hud_group = hud_group
        self.hud_elements = hud_elements

        # set player data
        self.player_data = player_data
        self.max_health = self.player_data['max_health']
        self.current_health = self.player_data['current_health']
        self.player_speed = self.player_data['player_speed']
        self.player_damage = self.player_data['player_damage']

        # create the initial HUD objects
        self.create_hud()

    # create HUD objects for the players stats_____________________________________________________
    def create_hud(self):
        hud_size = (64, 64)
        screen = pygame.display.get_surface()

        # health bar for maximum amount of health
        max_health_bar_surface = pygame.Surface((self.max_health, 10))
        max_health_bar_surface.fill((255, 255, 255))
        max_health_bar = HUDobject((20, 20), max_health_bar_surface, self.hud_group, 'max_health_bar')
        self.hud_elements['max_health_bar'] = max_health_bar

        # health bar for players current health
        current_health_bar_surface = pygame.Surface((self.current_health, 10))
        current_health_bar_surface.fill((255, 0, 0))
        current_health_bar = HUDobject((20, 20), current_health_bar_surface, self.hud_group, 'current_health_bar')
        self.hud_elements['current_health_bar'] = current_health_bar

        # create the damage stat icon
        damage_stat_image = pygame.image.load('textures/32X32/HUD/damage_stat.png').convert()
        damage_stat_image = pygame.transform.scale(damage_stat_image, hud_size)
        damage_stat_icon = HUDobject((screen.get_width() - (hud_size[0] + 20), 20),
                                     damage_stat_image, self.hud_group, 'damage_icon')
        self.hud_elements['damage_icon'] = damage_stat_icon

        # create the damage stat text
        damage_stat = Text((damage_stat_icon.rect.centerx, damage_stat_icon.rect.centery + 15),
                           self.player_damage, self.hud_group, 30, (255, 255, 255), 'damage_stat')
        self.hud_elements['damage_stat'] = damage_stat

        # create the movement speed stat icon
        movement_speed_stat_image = pygame.image.load('textures/32X32/HUD/movement_speed_stat.png').convert()
        movement_speed_stat_image = pygame.transform.scale(movement_speed_stat_image, hud_size)
        movement_speed_stat_icon = HUDobject((screen.get_width() - (hud_size[0] + 20) * 2, 20),
                                             movement_speed_stat_image, self.hud_group, 'speed_icon')
        self.hud_elements['speed_icon'] = movement_speed_stat_icon

        # create the movement speed stat text
        movement_speed_stat = Text((movement_speed_stat_icon.rect.centerx, movement_speed_stat_icon.rect.centery + 15),
                                   self.player_speed, self.hud_group, 30, (255, 255, 255), 'movement_speed_stat')
        self.hud_elements['movement_speed_stat'] = movement_speed_stat

        # hud icon to open the players inventory
        inventory_icon_image = pygame.image.load('textures/32X32/HUD/inventory_button.png').convert()
        inventory_icon_image = pygame.transform.scale(inventory_icon_image, hud_size)
        inventory_icon = HUDobject((20, 50), inventory_icon_image, self.hud_group, 'inventory_icon')
        self.hud_elements['inventory_icon'] = inventory_icon

        # hud icon to open the players setting menu
        inventory_icon_image = pygame.image.load('textures/32X32/HUD/settings_icon.png').convert()
        inventory_icon_image = pygame.transform.scale(inventory_icon_image, hud_size)
        inventory_icon = HUDobject((20, 114), inventory_icon_image, self.hud_group, 'setting_icon')
        self.hud_elements['setting_icon'] = inventory_icon

        # Mobile controls______________________________________________
        # Up movement button
        up_arrow_image = pygame.image.load('textures/32X32/HUD/move_arrow.png').convert()
        up_arrow_image = pygame.transform.scale(up_arrow_image, (hud_size[0]*2, hud_size[1]*2))
        up_arrow_icon = HUDobject((168, screen.get_height() - 294), up_arrow_image,
                                  self.hud_group, 'mobile')
        self.hud_elements['up_arrow'] = up_arrow_icon

        # right movement button
        right_arrow_image = pygame.image.load('textures/32X32/HUD/move_arrow.png').convert()
        right_arrow_image = pygame.transform.scale(right_arrow_image, (hud_size[0]*2, hud_size[1]*2))
        right_arrow_image = pygame.transform.rotate(right_arrow_image, 270)
        right_arrow_icon = HUDobject((314, screen.get_height() - 148), right_arrow_image,
                                     self.hud_group, 'mobile')
        self.hud_elements['right_arrow'] = right_arrow_icon

        # down movement button
        down_arrow_image = pygame.image.load('textures/32X32/HUD/move_arrow.png').convert()
        down_arrow_image = pygame.transform.scale(down_arrow_image, (hud_size[0]*2, hud_size[1]*2))
        down_arrow_image = pygame.transform.rotate(down_arrow_image, 180)
        down_arrow_icon = HUDobject((168, screen.get_height() - 148), down_arrow_image,
                                    self.hud_group, 'mobile')
        self.hud_elements['down_arrow'] = down_arrow_icon

        # left movement button
        left_arrow_image = pygame.image.load('textures/32X32/HUD/move_arrow.png').convert()
        left_arrow_image = pygame.transform.scale(left_arrow_image, (hud_size[0]*2, hud_size[1]*2))
        left_arrow_image = pygame.transform.rotate(left_arrow_image, 90)
        left_arrow_icon = HUDobject((20, screen.get_height() - 148), left_arrow_image,
                                    self.hud_group, 'mobile')
        self.hud_elements['left_arrow'] = left_arrow_icon

        # up attack button
        up_attack_image = pygame.image.load('textures/32X32/HUD/attack_arrow.png').convert()
        up_attack_image = pygame.transform.scale(up_attack_image, (hud_size[0] * 2, hud_size[1] * 2))
        up_attack_icon = HUDobject((screen.get_width()-296, screen.get_height() - 294), up_attack_image,
                                   self.hud_group, 'mobile')
        self.hud_elements['up_attack'] = up_attack_icon

        # right attack button
        right_attack_image = pygame.image.load('textures/32X32/HUD/attack_arrow.png').convert()
        right_attack_image = pygame.transform.scale(right_attack_image, (hud_size[0] * 2, hud_size[1] * 2))
        right_attack_image = pygame.transform.rotate(right_attack_image, 270)
        right_attack_icon = HUDobject((screen.get_width()-144, screen.get_height() - 148), right_attack_image,
                                      self.hud_group, 'mobile')
        self.hud_elements['right_attack'] = right_attack_icon

        # down attack button
        down_attack_image = pygame.image.load('textures/32X32/HUD/attack_arrow.png').convert()
        down_attack_image = pygame.transform.scale(down_attack_image, (hud_size[0] * 2, hud_size[1] * 2))
        down_attack_image = pygame.transform.rotate(down_attack_image, 180)
        down_attack_icon = HUDobject((screen.get_width()-296, screen.get_height() - 148), down_attack_image,
                                     self.hud_group, 'mobile')
        self.hud_elements['down_attack'] = down_attack_icon

        # left attack button
        left_attack_image = pygame.image.load('textures/32X32/HUD/attack_arrow.png').convert()
        left_attack_image = pygame.transform.scale(left_attack_image, (hud_size[0] * 2, hud_size[1] * 2))
        left_attack_image = pygame.transform.rotate(left_attack_image, 90)
        left_attack_icon = HUDobject((screen.get_width()-442, screen.get_height() - 148), left_attack_image, self.hud_group, 'mobile')
        self.hud_elements['left_attack'] = left_attack_icon

    # update the position of hud elements match the screen size____________________________________
    def update_hud(self):
        hud_size = (64, 64)
        screen = pygame.display.get_surface()
        self.hud_elements['damage_icon'].rect.topleft = (screen.get_width() - (hud_size[0] + 20), 20)
        self.hud_elements['damage_stat'].rect.center = (self.hud_elements['damage_icon'].rect.centerx,
                                                        self.hud_elements['damage_icon'].rect.centery + 15)

        self.hud_elements['speed_icon'].rect.topleft = (screen.get_width() - (hud_size[0] + 20) * 2, 20)
        self.hud_elements['movement_speed_stat'].rect.center = (self.hud_elements['speed_icon'].rect.centerx,
                                                                self.hud_elements['speed_icon'].rect.centery + 15)

    def mobile_controls(self):
        hud_size = (64, 64)

