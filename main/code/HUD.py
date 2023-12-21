import pygame
from sprites import HUD_object, Text


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
        max_health_bar = HUD_object((20, 20), max_health_bar_surface, self.hud_group, 'max_health_bar')
        self.hud_elements['max_health_bar'] = max_health_bar

        # health bar for players current health
        current_health_bar_surface = pygame.Surface((self.current_health, 10))
        current_health_bar_surface.fill((255, 0, 0))
        current_health_bar = HUD_object((20, 20), current_health_bar_surface, self.hud_group, 'current_health_bar')
        self.hud_elements['current_health_bar'] = current_health_bar

        # create the damage stat icon
        damage_stat_image = pygame.image.load('../textures/32X32/HUD/damage_stat.png').convert()
        damage_stat_image = pygame.transform.scale(damage_stat_image, hud_size)
        damage_stat_icon = HUD_object((screen.get_width() - (hud_size[0] + 20), 20),
                                      damage_stat_image, self.hud_group, 'damage_icon')
        self.hud_elements['damage_icon'] = damage_stat_icon

        # create the damage stat text
        damage_stat = Text((damage_stat_icon.rect.centerx, damage_stat_icon.rect.centery + 15),
                           self.player_damage, self.hud_group, 30, (255, 255, 255), 'damage_stat')
        self.hud_elements['damage_stat'] = damage_stat

        # create the movement speed stat icon
        movement_speed_stat_image = pygame.image.load('../textures/32X32/HUD/movement_speed_stat.png').convert()
        movement_speed_stat_image = pygame.transform.scale(movement_speed_stat_image, hud_size)
        movement_speed_stat_icon = HUD_object((screen.get_width() - (hud_size[0] + 20) * 2, 20),
                                              movement_speed_stat_image, self.hud_group, 'speed_icon')
        self.hud_elements['speed_icon'] = movement_speed_stat_icon

        # create the movement speed stat text
        movement_speed_stat = Text((movement_speed_stat_icon.rect.centerx, movement_speed_stat_icon.rect.centery + 15),
                                   self.player_speed, self.hud_group, 30, (255, 255, 255), 'movement_speed_stat')
        self.hud_elements['movement_speed_stat'] = movement_speed_stat

        # hud icon to open the players inventory
        inventory_icon_image = pygame.image.load('../textures/32X32/HUD/inventory_button.png').convert()
        inventory_icon_image = pygame.transform.scale(inventory_icon_image, hud_size)
        inventory_icon = HUD_object((20, 50), inventory_icon_image, self.hud_group, 'inventory_icon')
        self.hud_elements['inventory_icon'] = inventory_icon

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
