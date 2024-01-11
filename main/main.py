import pygame
import asyncio
import time
from pygame.locals import *
from config import *
from dungeon_generator import Dungeon
from player import Player
from enemy_spawner import EnemySpawner
from sprites import Text
from tile_system import Grid
from main_menu import MenuScreens
from dialog_system import Dialog

# start pygame_____________________________________________________________________________________
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
pygame.display.set_caption('Vorpal Dive')
running = True
clock = pygame.time.Clock()


# A class to hold all the games states and variables_______________________________________________
class GameVariables:
    def __init__(self):
        self.in_game = False
        self.in_main_menu = True

        # initiate the game
        self.grid = None
        self.dialog = None
        self.dungeon = None
        self.player = None
        self.enemy_spawner = None
        self.debug = None

    # reset the game
    def clear_game(self):
        self.in_game = False
        self.in_main_menu = True

        visible_group.empty()
        hud_group.empty()
        obstacle_group.empty()
        weapon_group.empty()
        enemy_group.empty()
        item_group.empty()
        interactable_group.empty()

    # initiate the game
    def start_game(self):
        self.grid = Grid()
        self.dialog = Dialog()
        self.dungeon = Dungeon(visible_group, obstacle_group, item_group, interactable_group, self.grid)
        self.player = Player(visible_group, self.dungeon.player_start_position, self.grid, visible_group,
                             obstacle_group, weapon_group, enemy_group, hud_group, item_group, interactable_group,
                             self.dialog)
        self.enemy_spawner = EnemySpawner(self.dungeon.floor_tile_positions, self.grid, visible_group,
                                          enemy_group, obstacle_group, weapon_group)

        self.debug = Text((screen_width - 75, screen_height - 75), str(round(clock.get_fps())), hud_group, 50,
                          (255, 255, 255))


# Custom Camera Group Setup________________________________________________________________________
class VisibleGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2(0, 0)
        self.ground_image = None

    # Center the camera on the player
    def center_camera(self, target):
        self.offset.x = target.rect.centerx - pygame.display.get_surface().get_width() // 2
        self.offset.y = target.rect.centery - pygame.display.get_surface().get_height() // 2

    # Draw all sprites on the screen
    def custom_draw(self):
        screen = pygame.display.get_surface()
        global dungeon
        self.center_camera(game_variable.player)

        # Display Ground before other items
        ground_offset = (0, 7) - self.offset
        screen.blit(game_variable.dungeon.dungeon_level[0], ground_offset)

        # Display items in relation to players character
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if (abs(sprite.rect.topleft[0] - game_variable.player.rect.topleft[0]) <= (screen.get_width() // 2) + tile_size and
                    abs(sprite.rect.topleft[1] - game_variable.player.rect.topleft[1]) <= (screen.get_height() // 2) + tile_size):
                offset_pos = sprite.rect.topleft - self.offset
                screen.blit(sprite.image, offset_pos)


class HUDGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    # custom draw function to allow only specific objects to be drawn______________________________
    def custom_draw(self, screen):
        for sprite in self.sprites():
            if sprite.name != 'mobile':
                screen.blit(sprite.image, sprite.rect)
            elif game_variable.player.mobile_mode:
                screen.blit(sprite.image, sprite.rect)


# Declare groups___________________________________________________________________________________
visible_group = VisibleGroup()
hud_group = HUDGroup()
obstacle_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
interactable_group = pygame.sprite.Group()


# open up the main menu
def main_menu():
    return MenuScreens()


last_frame_time = time.time()
game_variable = GameVariables()


async def main():
    global running, last_frame_time, game_variable
    menu = main_menu()

    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        dt = (time.time() - last_frame_time) * 60
        last_frame_time = time.time()

        if game_variable.in_game:
            screen.fill((0, 0, 0))
            visible_group.custom_draw()
            game_variable.player.update(event_list, dt)

            game_variable.enemy_spawner.decide_spawn_enemy(game_variable.player.rect.center)
            enemy_group.update(game_variable.player.rect.center, dt)
            game_variable.debug.image = pygame.font.Font(None, 50).render((str(round(clock.get_fps()))), True, (255, 255, 255))

            hud_group.custom_draw(screen)
            game_variable.dialog.display_dialog(event_list, game_variable)

        if game_variable.in_main_menu:
            selection = menu.draw(event_list)
            if selection == 'start_game':
                game_variable.in_game = True
                game_variable.in_main_menu = False
                pygame.display.flip()
                game_variable.start_game()

        pygame.display.flip()
        clock.tick()
        await asyncio.sleep(0)


asyncio.run(main())
