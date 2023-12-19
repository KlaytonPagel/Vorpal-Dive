import pygame
from config import *
from dungeon_generator import Dungeon
from player import Player
from Debug import debug
from enemy_spawner import EnemySpawner

# start pygame_____________________________________________________________________________________
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('py dungeon')
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
        self.offset.x = target.rect.centerx - screen_width // 2
        self.offset.y = target.rect.centery - screen_height // 2

    # Draw all sprites on the screen
    def custom_draw(self):
        if self.ground_image is None:
            self.ground_image = pygame.image.load('../complete_floors/complete_floor.png').convert()
        self.center_camera(player)

        # Display Ground before other items
        ground_offset = (0, 7) - self.offset
        screen.blit(self.ground_image, ground_offset)

        # Display items in relation to players character
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)


# Declare groups___________________________________________________________________________________
visible_group = VisibleGroup()
obstacle_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
hud_group = pygame.sprite.Group()

# create objects___________________________________________________________________________________
dungeon = Dungeon(visible_group, obstacle_group)
player = Player(visible_group, dungeon.player_start_position, screen, visible_group,
                obstacle_group, projectile_group, enemy_group, hud_group)
enemy_spawner = EnemySpawner(dungeon.floor_tile_positions, visible_group, enemy_group, obstacle_group, projectile_group)


while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    visible_group.custom_draw()
    player.update(event_list)
    debug(str(round(clock.get_fps())))

    enemy_spawner.decide_spawn_enemy(player.rect.center)
    enemy_group.update(player.rect.center)

    hud_group.draw(screen)

    pygame.display.flip()
    clock.tick(fps)
