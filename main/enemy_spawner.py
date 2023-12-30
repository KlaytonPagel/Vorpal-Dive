import time
import random_number as random
from config import *
from enemy import Enemy


# Class to spawn enemies in the dungeon____________________________________________________________
class EnemySpawner:
    def __init__(self, spawnable_tiles, grid, visible_group, enemy_group, obstacle_group, projectile_group):
        self.spawnable_tiles = spawnable_tiles
        self.visible_group = visible_group
        self.enemy_group = enemy_group
        self.obstacle_group = obstacle_group
        self.projectile_group = projectile_group
        self.grid = grid

        self.can_spawn = True
        self.spawn_cooldown = time.time()

    # Spawn an enemy on a floor tile not close to the player_______________________________________
    def spawn_enemy(self, player_location):
        enemy_location = self.spawnable_tiles[random.randint(0, len(self.spawnable_tiles) - 1)]
        if (abs(player_location[0] - enemy_location[0]) <= 10 * tile_size and
                abs(player_location[1] - enemy_location[1]) <= 10 * tile_size):
            self.spawn_enemy(player_location)
        else:
            Enemy((self.visible_group, self.enemy_group), enemy_location, self.grid, self.obstacle_group, self.projectile_group)

    # Decide weather to spawn an enemy or not______________________________________________________
    def decide_spawn_enemy(self, player_location):

        # enemy spawning cooldown
        if not self.can_spawn:
            current_time = time.time()
            if current_time - self.spawn_cooldown >= 1:
                self.can_spawn = True

        # try to spawn an enemy based off of spawn chance in the config
        else:
            if random.randint(1, 100/spawn_chance_per_second) == 1:
                for i in range(1):
                    self.spawn_enemy(player_location)
            self.can_spawn = False
            self.spawn_cooldown = time.time()
