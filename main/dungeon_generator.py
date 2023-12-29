import random_number as random
import pygame
from sprites import Tile
from config import *


# Dungeon class for generating a random dungeon____________________________________________________
class Dungeon:
    def __init__(self, visible_group, obstacle_group):
        self.floor_tile_positions = []
        self.visible_group = visible_group
        self.obstacle_group = obstacle_group
        self.player_start_position = None
        self.dungeon_level = []
        self.generate_rooms()

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

                # Build out the room from the starting position
                for h in range(room_height):
                    for w in range(room_width):
                        self.floor_tile_positions.append((room_x + w * tile_size, room_y + h * tile_size))

                # if this is not the first room, create a tunnel to the previous room
                start_position = (room_x + room_width // 2 * tile_size, room_y + room_height // 2 * tile_size)
                if end_position is not None:
                    self.create_tunnel(start_position, end_position)
                else: self.player_start_position = start_position
                end_position = (room_x + room_width // 2 * tile_size, room_y + room_height // 2 * tile_size)

        # Place wall and floor images
        self.build_floors()
        self.build_walls()

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

        # load all floor tile images and combine all tiles onto one surface
        floor_tile_image = pygame.image.load('textures/32X32/Floors/Floor 3.png')
        floor_tile_image = pygame.transform.scale(floor_tile_image, (tile_size, tile_size))
        for tile in self.floor_tile_positions:
            complete_floor_surface.blit(floor_tile_image, (tile[0], tile[1]))
        self.dungeon_level.append(complete_floor_surface)

    # Check if tiles adjacent to occupied tiles are also occupied, if not put a wall tile down_____
    def build_walls(self):
        wall_image = 'textures/32X32/Walls/Wall front.png'
        for tile in self.floor_tile_positions:

            # Check tile to the right
            if (tile[0] + tile_size, tile[1]) not in self.floor_tile_positions:
                Tile((tile[0] + tile_size, tile[1]),
                        wall_image, (self.visible_group, self.obstacle_group))

            # check tile to the left
            if (tile[0] - tile_size, tile[1]) not in self.floor_tile_positions:
                Tile((tile[0] - tile_size, tile[1]),
                        wall_image, (self.visible_group, self.obstacle_group))

            # check tile above
            if (tile[0], tile[1] + tile_size) not in self.floor_tile_positions:
                Tile((tile[0], tile[1] + tile_size),
                        wall_image, (self.visible_group, self.obstacle_group))

            # check tile below
            if (tile[0], tile[1] - tile_size) not in self.floor_tile_positions:
                Tile((tile[0], tile[1] - tile_size),
                        wall_image, (self.visible_group, self.obstacle_group))
