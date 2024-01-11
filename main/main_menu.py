import time
import pygame
from sprites import Tile


# A class for the players main menu screen
class MenuScreens:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.menu_group = pygame.sprite.Group()
        self.menu_items = {}
        self.button_cool_down = time.time()
        self.on_cool_down = True

        self.play_button_pressed = pygame.image.load('textures/32X32/play_button_pressed.png').convert()
        self.play_button_image = pygame.image.load('textures/32X32/play_button.png').convert()
        self.play_button_down = pygame.image.load('textures/32X32/play_button_down.png').convert_alpha()
        self.play_button_status = 'unpressed'

        self.create_main_menu()

    # initialize all main menu elements
    def create_main_menu(self):
        menu_image = pygame.image.load('textures/32X32/main_menu.png').convert_alpha()
        main_menu_sprite = Tile((0, 0), menu_image, self.menu_group,
                                sprite_size=(self.screen.get_width(), self.screen.get_height() // 3))
        self.menu_items['main_menu'] = main_menu_sprite

        play_button_sprite = Tile((100, self.screen.get_height() // 2), self.play_button_image, self.menu_group,
                                  sprite_size=(self.screen.get_width() // 4, self.screen.get_height() // 3))
        self.menu_items['play_button'] = play_button_sprite

    # detect all input from the player
    def user_input(self, event_list):
        for event in event_list:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.menu_items['play_button'].rect.collidepoint(mouse_x, mouse_y) and self.play_button_status == 'unpressed':
                self.menu_items['play_button'].image = self.play_button_pressed
                self.play_button_status = 'pressed'
            if not self.menu_items['play_button'].rect.collidepoint(mouse_x, mouse_y) and self.play_button_status == 'pressed':
                self.menu_items['play_button'].image = self.play_button_image
                self.play_button_status = 'unpressed'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.on_cool_down:
                x, y = event.pos

                if self.menu_items['play_button'].rect.collidepoint(x, y):
                    self.menu_items['play_button'].image = self.play_button_down
                    return 'start_game'

    # update the menu to fit the players screen
    def update_main_menu(self):
        self.cool_downs()
        self.menu_items['main_menu'].image = pygame.transform.scale(self.menu_items['main_menu'].image,
                                                                    (self.screen.get_width(),
                                                                     self.screen.get_height() // 3))

        self.menu_items['play_button'].image = pygame.transform.scale(self.menu_items['play_button'].image,
                                                                      (self.screen.get_width() // 4,
                                                                       self.screen.get_height() // 3))

        self.menu_items['play_button'].rect.topleft = (100, self.screen.get_height() // 2)

    # draw the menu on to the players screen
    def draw(self, event_list):
        selection = self.user_input(event_list)
        self.update_main_menu()
        self.screen.fill((100, 100, 100))
        self.menu_group.draw(self.screen)
        if selection == 'start_game':
            return selection

    # cool down so players don't accidentally press the button right away
    def cool_downs(self):
        if self.on_cool_down:
            current_time = time.time()
            if current_time - self.button_cool_down > 1:
                self.on_cool_down = False
