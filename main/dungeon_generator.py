import random_number as random
import pygame
from sprites import Tile
from config import *
from item_system import Item


# Dungeon class for generating a random dungeon____________________________________________________
class Dungeon:
    def __init__(self, visible_group, obstacle_group, item_group, grid):
        self.floor_tile_positions = []
        self.wall_tile_positions = {}
        self.wall_tile_sprites = {}
        self.grid = grid
        self.visible_group = visible_group
        self.obstacle_group = obstacle_group
        self.item_group = item_group
        self.player_start_position = None
        self.dungeon_level = []
        self.room_centers = []
        self.generate_rooms()
        self.build_floors()
        self.build_walls()
        self.spawn_artifact()

    # Choose random places within dungeon size and build rooms_____________________________________
    def generate_rooms(self):
        end_position = None
        for attempt in range(room_attempts):

            # Pick a random point to create a room
            room_x = random.randint(0, dungeon_width - (max_room_width * tile_size))
            room_y = random.randint(0, dungeon_height - (max_room_height * tile_size))

            # align the room to a grid of tiles based on the tile size
            if room_x % tile_size != 0:
                room_x -= room_x % tile_size
            if room_y % tile_size != 0:
                room_y -= room_y % tile_size

            # randomize the room height and width based off of the defined max and min height and width
            room_width = random.randint(min_room_width, max_room_width)
            room_height = random.randint(min_room_height, max_room_height)

            # Check if a room will overlap
            if self.validate_room(room_x, room_y, room_width, room_height):
                # add room center to list for spawning items
                self.room_centers.append((room_x + room_width // 2 * tile_size, room_y + room_height // 2 * tile_size))

                # Build out the room from the starting position
                for h in range(room_height):
                    for w in range(room_width):
                        self.floor_tile_positions.append((room_x + w * tile_size, room_y + h * tile_size))

                # if this is not the first room, create a tunnel to the previous room
                start_position = (room_x + room_width // 2 * tile_size, room_y + room_height // 2 * tile_size)
                if end_position is not None:
                    self.create_tunnel(start_position, end_position)
                else:
                    self.player_start_position = start_position
                end_position = (room_x + room_width // 2 * tile_size, room_y + room_height // 2 * tile_size)

    # Checks if there are already tiles in any of the spots the room will occupy___________________
    def validate_room(self, room_x, room_y, room_width, room_height):
        for h in range(1, room_height):
            for w in range(1, room_width):
                if (room_x + w * tile_size, room_y + h * tile_size) in self.floor_tile_positions:
                    return False
        return True

    # Create tunnel from the current room to the previously made room______________________________
    def create_tunnel(self, start_position, end_position):
        start_x, start_y = start_position
        end_x, end_y = end_position

        # travel from the start to the end point on the x-axis
        while start_x != end_x:
            if start_x < end_x:
                start_x += tile_size
            else:
                start_x -= tile_size

            # place floor tiles for the tunnel at the defined width
            start_y -= tile_size
            for i in range(tunnel_width):
                if (start_x, start_y) not in self.floor_tile_positions:
                    self.floor_tile_positions.append((start_x, start_y))
                start_y += tile_size
            start_y -= tile_size * (tunnel_width - 1)

        # travel from the start to the end point on the y-axis
        while start_y != end_y:
            if start_y < end_y:
                start_y += tile_size
            else:
                start_y -= tile_size

            # place floor tiles for the tunnel at the defined width
            start_x -= tile_size
            for i in range(tunnel_width):
                if (start_x, start_y) not in self.floor_tile_positions:
                    self.floor_tile_positions.append((start_x, start_y))
                start_x += tile_size
            start_x -= tile_size * (tunnel_width - 1)

    # combine all floor tiles into one image and save it___________________________________________
    def build_floors(self):
        # Create a new surface for all floor tiles
        complete_floor_surface = pygame.Surface((dungeon_width, dungeon_height))
        floor_images = ['textures/32X32/Floors/floor_bottom_right.png',
                        'textures/32X32/Floors/floor_bottom_left.png',
                        'textures/32X32/Floors/floor_top_left.png',
                        'textures/32X32/Floors/floor_top_right.png',
                        'textures/32X32/Floors/floor_horizontal.png',
                        'textures/32X32/Floors/floor_vertical.png']

        for tile in self.floor_tile_positions:
            # load all floor tile images and combine all tiles onto one surface
            floor_tile_image = pygame.image.load(floor_images[random.randint(0, len(floor_images) - 1)]).convert()
            floor_tile_image = pygame.transform.scale(floor_tile_image, (tile_size, tile_size))
            complete_floor_surface.blit(floor_tile_image, (tile[0], tile[1]))
        self.dungeon_level.append(complete_floor_surface)

    # Check if tiles adjacent to occupied tiles are also occupied, if not put a wall tile down_____
    def build_walls(self):
        wall_front_image = pygame.image.load('textures/32X32/Walls/wall_front.png').convert_alpha()
        wall_left_image = pygame.image.load('textures/32X32/Walls/wall_left.png').convert_alpha()
        wall_right_image = pygame.image.load('textures/32X32/Walls/wall_right.png').convert_alpha()
        wall_top_left_image = pygame.image.load('textures/32X32/Walls/wall_top_left.png').convert_alpha()
        wall_top_right_image = pygame.image.load('textures/32X32/Walls/wall_top_right.png').convert_alpha()
        wall_bottom_left_image = pygame.image.load('textures/32X32/Walls/wall_bottom_left.png').convert_alpha()
        wall_bottom_right_image = pygame.image.load('textures/32X32/Walls/wall_bottom_right.png').convert_alpha()
        wall_top_long_left_image = pygame.image.load('textures/32X32/Walls/wall_top_long_left.png').convert_alpha()
        wall_top_long_right_image = pygame.image.load('textures/32X32/Walls/wall_top_long_right.png').convert_alpha()
        wall_bottom_long_left_image = pygame.image.load(
            'textures/32X32/Walls/wall_bottom_long_left.png').convert_alpha()
        wall_bottom_long_right_image = pygame.image.load(
            'textures/32X32/Walls/wall_bottom_long_right.png').convert_alpha()
        wall_top_connect_image = pygame.image.load('textures/32X32/Walls/wall_top_connect.png').convert_alpha()
        wall_bottom_connect_image = pygame.image.load('textures/32X32/Walls/wall_bottom_connect.png').convert_alpha()

        for tile in self.floor_tile_positions:

            # top right corner
            if ((tile[0] + tile_size, tile[1]) not in self.floor_tile_positions
                    and (tile[0], tile[1] - tile_size) not in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] - tile_size) not in self.floor_tile_positions):
                position = (tile[0] + tile_size, tile[1] - tile_size)
                side = 'default'
                self.wall_tile_positions[position] = [wall_top_right_image, side]

            # top left corner
            if ((tile[0] - tile_size, tile[1]) not in self.floor_tile_positions
                    and (tile[0], tile[1] - tile_size) not in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] - tile_size) not in self.floor_tile_positions):
                position = (tile[0], tile[1])
                side = 'top left'
                self.wall_tile_positions[position] = [wall_top_left_image, side]

            # bottom right corner
            if ((tile[0] + tile_size, tile[1]) not in self.floor_tile_positions
                    and (tile[0], tile[1] + tile_size) not in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0] + tile_size, tile[1] + tile_size)
                side = 'bottom right'
                self.wall_tile_positions[position] = [wall_bottom_right_image, side]

            # bottom left corner
            if ((tile[0] - tile_size, tile[1]) not in self.floor_tile_positions
                    and (tile[0], tile[1] + tile_size) not in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0], tile[1] + tile_size)
                side = 'bottom left'
                self.wall_tile_positions[position] = [wall_bottom_left_image, side]

                if (tile[0] + tile_size, tile[1] + tile_size) in self.floor_tile_positions:
                    position = (tile[0] + tile_size // 2, tile[1] + tile_size)
                    side = 'bottom'
                    self.wall_tile_positions[position] = [wall_top_long_right_image, side]

            # top connect
            if ((tile[0] + tile_size, tile[1] + tile_size) in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] + tile_size) in self.floor_tile_positions
                    and (tile[0], tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0], tile[1] + tile_size)
                side = 'default'
                self.wall_tile_positions[position] = [wall_top_connect_image, side]

            # bottom connect
            if ((tile[0] + tile_size, tile[1] - tile_size) in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] - tile_size) in self.floor_tile_positions
                    and (tile[0], tile[1] - tile_size) not in self.floor_tile_positions):
                position = (tile[0], tile[1] - tile_size)
                side = 'default'
                self.wall_tile_positions[position] = [wall_bottom_connect_image, side]

            # bottom left inside corner
            if ((tile[0], tile[1] - tile_size) in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1]) in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] - tile_size) not in self.floor_tile_positions):
                position = (tile[0] + tile_size, tile[1] - tile_size)
                side = 'default'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_bottom_long_left_image, side]

            # bottom right inside corner
            if ((tile[0], tile[1] - tile_size) in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1]) in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] - tile_size) not in self.floor_tile_positions):
                position = (tile[0] - tile_size, tile[1] - tile_size)
                side = 'default'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_bottom_long_right_image, side]

            # top left inside corner
            if ((tile[0], tile[1] + tile_size) in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1]) in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0] + tile_size, tile[1] + tile_size)
                side = 'default'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_top_long_left_image, side]

            # top right inside corner
            if ((tile[0], tile[1] + tile_size) in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1]) in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0] - tile_size, tile[1] + tile_size)
                side = 'default'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_top_long_right_image, side]

            # bottom
            if ((tile[0], tile[1] + tile_size) not in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] + tile_size) not in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0] + tile_size // 2, tile[1] + tile_size)
                side = 'bottom'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_front_image, side]

            # top
            if ((tile[0], tile[1] - tile_size) not in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] - tile_size) not in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] - tile_size) not in self.floor_tile_positions):
                position = (tile[0] + tile_size // 2, tile[1])
                side = 'top'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_front_image, side]

            # left
            if ((tile[0] - tile_size, tile[1]) not in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] - tile_size) not in self.floor_tile_positions
                    and (tile[0] - tile_size, tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0], tile[1] + tile_size // 2)
                side = 'left'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_left_image, side]

            # right
            if ((tile[0] + tile_size, tile[1]) not in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] - tile_size) not in self.floor_tile_positions
                    and (tile[0] + tile_size, tile[1] + tile_size) not in self.floor_tile_positions):
                position = (tile[0] + tile_size, tile[1] + tile_size // 2)
                side = 'right'
                if position in self.wall_tile_positions:
                    pass
                else:
                    self.wall_tile_positions[position] = [wall_right_image, side]

        # Check the walls situation and apply the correct image
        for position, data in self.wall_tile_positions.items():
            wall = Tile(position, data[0], (self.visible_group, self.obstacle_group), data[1])
            self.wall_tile_sprites[position] = wall

        self.populate_grid_tiles()

    def populate_grid_tiles(self):
        for position, wall in self.wall_tile_sprites.items():
            self.grid.fill_grid(position, wall)

    def spawn_artifact(self):
        artifact_image = pygame.image.load('textures/32X32/green_drop.png').convert_alpha()

        room_index = random.randint(0, len(self.room_centers) - 1)
        if (abs(self.room_centers[room_index][0] - self.player_start_position[0]) < dungeon_width // 2 and
                abs(self.room_centers[room_index][1] - self.player_start_position[1]) < dungeon_height // 2):
            self.spawn_artifact()

        else:
            artifact = Item((self.visible_group, self.item_group), artifact_image, self.room_centers[room_index])
