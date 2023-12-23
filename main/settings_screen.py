import pygame
from sprites import HUDobject


class Settings:
    def __init__(self):
        self.settings_options = {}
        self.screen = pygame.display.get_surface()
        self.settings_group = pygame.sprite.Group()
        self.create_settings()

    def create_settings(self):
        # settings menu image
        settings_image = pygame.image.load('textures/32X32/HUD/settings_menu.png').convert_alpha()
        HUDobject((84, 50), settings_image, self.settings_group)

        # Mobile mode settings check box
        mobile_mode_box_image = pygame.image.load('textures/32X32/HUD/blank.png').convert_alpha()
        mobile_mode_box = HUDobject((88, 55), mobile_mode_box_image, self.settings_group, 'mobile_mode')
        self.settings_options['mobile_mode'] = mobile_mode_box

    def update_settings_menu(self, mobile_mode):
        unchecked_box = pygame.image.load('textures/32X32/HUD/blank.png').convert_alpha()
        checked_box = pygame.image.load('textures/32X32/HUD/check_box.png').convert_alpha()
        if mobile_mode:
            self.settings_options['mobile_mode'].image = checked_box
        if not mobile_mode:
            self.settings_options['mobile_mode'].image = unchecked_box
        self.settings_group.draw(self.screen)
