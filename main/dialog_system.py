import pygame


# class for giving the user dialog and responses to select from____________________________________
class Dialog:
    def __init__(self):
        self.blank_box = pygame.image.load('textures/32X32/blank_dialog_box.png').convert()
        self.screen = pygame.display.get_surface()
        self.dialog = []
        self.response = {}

    # display the dialog to the user
    def display_dialog(self, event_list, game_variable):
        self.user_input(event_list, game_variable)
        dialog_box_position = (0, self.screen.get_height() - self.screen.get_height()//3)
        dialog_box_size = (self.screen.get_width(), self.screen.get_height()//3)
        response_box_size = (self.screen.get_width() // 8, self.screen.get_height() // 8)
        response_box_position_2 = (0, self.screen.get_height() - self.screen.get_height()//3 - response_box_size[1])

        for item in self.dialog:
            item = pygame.transform.scale(item, dialog_box_size)
            self.screen.blit(item, dialog_box_position)

        for item, location in self.response.items():
            item.image = pygame.transform.scale(item.image, response_box_size)
            if location[0] == 'first':
                item.rect.bottomleft = dialog_box_position
            if location[0] == 'second':
                item.rect.bottomleft = response_box_position_2
            self.screen.blit(item.image, item.rect)

    # clear the dialog from the screen
    def clear_dialog(self):
        self.dialog = []
        self.response = {}

    # gather all user input for selecting the response option
    def user_input(self, event_list, game_variable):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                for button, action in self.response.items():
                    if button.rect.collidepoint(x, y) and action[1] == 'no':
                        self.clear_dialog()
                    if button.rect.collidepoint(x, y) and action[1] == 'leave':
                        game_variable.clear_game()
                        game_variable.open_menu()

    # Dialog for when the player interacts with the ladder to leave
    def ladder_dialog(self):
        text = 'Are you sure you would like to leave?'
        text_image = pygame.font.Font(None, 60)
        text_image = text_image.render(str(text), True, 'white')
        text_surface = self.blank_box
        text_surface.blit(text_image, (20, 20))
        self.dialog.append(text_surface)
        yes_response = Response('yes', (0, self.screen.get_height() - self.screen.get_height()//3))
        no_response = Response('no', yes_response.rect.topleft)
        self.response[yes_response] = ['first', 'leave']
        self.response[no_response] = ['second', 'no']


# A class used to make the sprites for the response buttons________________________________________
class Response(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        super().__init__()
        self.image = pygame.image.load('textures/32X32/blank_response_box.png').convert()
        self.image = pygame.transform.scale(self.image, (200, 100))
        text_image = pygame.font.Font(None, 60)
        text_image = text_image.render(str(text), True, 'white')
        self.image.blit(text_image, (20, 20))
        self.rect = self.image.get_rect(bottomleft=pos)
