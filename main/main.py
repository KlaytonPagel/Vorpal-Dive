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

# start pygame_____________________________________________________________________________________
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
pygame.display.set_caption('Vorpal Dive')
running = True
clock = pygame.time.Clock()


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
        self.center_camera(player)

        # Display Ground before other items
        ground_offset = (0, 7) - self.offset
        screen.blit(dungeon.dungeon_level[0], ground_offset)

        # Display items in relation to players character
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if (abs(sprite.rect.topleft[0] - player.rect.topleft[0]) <= (screen.get_width() // 2) + tile_size and
                    abs(sprite.rect.topleft[1] - player.rect.topleft[1]) <= (screen.get_height() // 2) + tile_size):
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
            elif player.mobile_mode:
                screen.blit(sprite.image, sprite.rect)


# Declare groups___________________________________________________________________________________
visible_group = VisibleGroup()
hud_group = HUDGroup()
obstacle_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# create objects___________________________________________________________________________________
grid = Grid()
dungeon = Dungeon(visible_group, obstacle_group, grid)
player = Player(visible_group, dungeon.player_start_position, grid, visible_group,
                obstacle_group, weapon_group, enemy_group, hud_group)
enemy_spawner = EnemySpawner(dungeon.floor_tile_positions, grid, visible_group,
                             enemy_group, obstacle_group, weapon_group)

debug = Text((screen_width - 75, screen_height - 75), str(round(clock.get_fps())), hud_group, 50, (255, 255, 255))

last_frame_time = time.time()


async def main():
    global running, last_frame_time

    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                player.save_player_data()
                player.inventory.save_inventory()
                running = False

        dt = (time.time() - last_frame_time) * 60
        last_frame_time = time.time()

        screen.fill((0, 0, 0))
        visible_group.custom_draw()
        player.update(event_list, dt)

        enemy_spawner.decide_spawn_enemy(player.rect.center)
        enemy_group.update(player.rect.center, dt)
        debug.image = pygame.font.Font(None, 50).render((str(round(clock.get_fps()))), True, (255, 255, 255))

        hud_group.custom_draw(screen)

        pygame.display.flip()
        clock.tick()
        await asyncio.sleep(0)


asyncio.run(main())
