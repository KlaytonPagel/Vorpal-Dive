import random
from tiles import Visible
from config import *


# Dungeon class for generating a random dungeon____________________________________________________
class Dungeon:
    def __init__(self, visible_group):
        self.occupied_tiles = []
        self.visible_group = visible_group
        self.generate_rooms()

    #
    def generate_rooms(self):
        end_position = None
        for attempt in range(room_attempts):

            # Pick a random point to create a room
            room_x = random.randint(0, dungeon_width)
            room_y = random.randint(0, dungeon_height)

            # align the room to a grid of tiles based on the tile size
            if room_x % tile_size != 0:
                room_x -= room_x % tile_size
            if room_y % tile_size != 0:
                room_y -= room_y % tile_size

            # randomize the room height and width based off of the defined max and min height and width
            room_width = random.randint(min_room_width, max_room_width) + 1
            room_height = random.randint(min_room_height, max_room_height) + 1

            # Check if a room will overlap
            if self.validate_room(room_x, room_y, room_width, room_height):

                # Build out the room from the starting position
                for h in range(1, room_height):
                    for w in range(1, room_width):
                        self.occupied_tiles.append((room_x + w * tile_size, room_y + h * tile_size))

                        # place the floor tiles for every room
                        Visible((room_x + w * tile_size, room_y + h * tile_size),
                                '../textures/32X32/Floors/Floor 2.png', self.visible_group)

                # if this is not the first room, create a tunnel to the previous room
                start_position = (room_x + room_width // 2 * tile_size, room_y + room_height // 2 * tile_size)
                if end_position is not None:
                    self.create_tunnel(start_position, end_position)
                end_position = (room_x + room_width // 2 * tile_size, room_y + room_height // 2 * tile_size)

        # build up walls around rooms and pathways
        self.build_walls()

    # Checks if there are already tiles in any of the spots the room will occupy
    def validate_room(self, room_x, room_y, room_width, room_height):
        for h in range(1, room_height):
            for w in range(1, room_width):
                if (room_x + w * tile_size, room_y + h * tile_size) in self.occupied_tiles:
                    return False
        return True

    # Create tunnel from the current room to the previously made room
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
                self.occupied_tiles.append((start_x, start_y))
                Visible((start_x, start_y),
                        '../textures/32X32/Floors/Floor 2.png', self.visible_group)
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
                self.occupied_tiles.append((start_x, start_y))
                Visible((start_x, start_y),
                        '../textures/32X32/Floors/Floor 2.png', self.visible_group)
                start_x += tile_size
            start_x -= tile_size * (tunnel_width - 1)

    def build_walls(self):
        for tile in self.occupied_tiles:
            if (tile[0] + tile_size, tile[1]) not in self.occupied_tiles:
                Visible((tile[0] + tile_size, tile[1]),
                        '../textures/32X32/Walls/Wall front.png', self.visible_group)

            if (tile[0] - tile_size, tile[1]) not in self.occupied_tiles:
                Visible((tile[0] - tile_size, tile[1]),
                        '../textures/32X32/Walls/Wall front.png', self.visible_group)

            if (tile[0], tile[1] + tile_size) not in self.occupied_tiles:
                Visible((tile[0], tile[1] + tile_size),
                        '../textures/32X32/Walls/Wall front.png', self.visible_group)

            if (tile[0], tile[1] - tile_size) not in self.occupied_tiles:
                Visible((tile[0], tile[1] - tile_size),
                        '../textures/32X32/Walls/Wall front.png', self.visible_group)
