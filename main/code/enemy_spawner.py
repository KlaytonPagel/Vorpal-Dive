import random
from config import *
from tiles import Visible


# Class to spawn enemies in the dungeon____________________________________________________________
class EnemySpawner:
    def __init__(self, spawnable_tiles, visible_group):
        self.spawnable_tiles = spawnable_tiles
        self.visible_group = visible_group

        self.can_spawn = True
        self.spawn_cooldown = fps

    # Spawn an enemy on a floor tile not close to the player_______________________________________
    def spawn_enemy(self, player_location):
        enemy_location = self.spawnable_tiles[random.randint(0, len(self.spawnable_tiles) - 1)]
        if (abs(player_location[0] - enemy_location[0]) <= 10 * tile_size and
                abs(player_location[1] - enemy_location[1]) <= 10 * tile_size):
            self.spawn_enemy(player_location)
        else:
            Visible(enemy_location, '../textures/Enemy.png', self.visible_group)

    # Decide weather to spawn an enemy or not
    def decide_spawn_enemy(self, player_location):
        if not self.can_spawn:
            self.spawn_cooldown += 1
            if self.spawn_cooldown >= fps:
                self.can_spawn = True
        else:
            print(random.randint(0, 100/spawn_chance_per_second))
            if random.randint(0, 100/spawn_chance_per_second) == 0:
                self.spawn_enemy(player_location)
            self.can_spawn = False
            self.spawn_cooldown = 0
