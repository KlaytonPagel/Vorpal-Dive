from config import *


class Grid:
    def __init__(self):
        self.grid_tile_size = tile_size * 3
        self.grid_size = ((dungeon_width // self.grid_tile_size) + 1, (dungeon_height // self.grid_tile_size) + 1)
        self.grid = {}
        self.make_grid()

    def make_grid(self):
        for grid_x in range(self.grid_size[0]):
            for grid_y in range(self.grid_size[1]):
                self.grid[grid_x, grid_y] = []

    def fill_grid(self, location, item):
        for grid_tile in self.grid:
            grid_start = (grid_tile[0] * self.grid_tile_size, grid_tile[1] * self.grid_tile_size)
            grid_end = (grid_start[0] + self.grid_tile_size, grid_start[1] + self.grid_tile_size)
            if grid_start[0] <= location[0] < grid_end[0] and grid_start[1] <= location[1] < grid_end[1]:
                self.grid[grid_tile].append(item)

    def get_grid_tile(self, location):
        for grid_tile in self.grid:
            grid_start = (grid_tile[0] * self.grid_tile_size, grid_tile[1] * self.grid_tile_size)
            grid_end = (grid_start[0] + self.grid_tile_size, grid_start[1] + self.grid_tile_size)
            if grid_start[0] <= location[0] < grid_end[0] and grid_start[1] <= location[1] < grid_end[1]:
                return grid_tile
