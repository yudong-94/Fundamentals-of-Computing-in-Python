"""
Clone of 2048 game.
"""

# http://www.codeskulptor.org/#user41_QyE846Od3EuryDW.py

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    valid_entry = []
    for entry in line:
        if entry != 0:
            valid_entry.append(entry)
    for index in range(len(valid_entry) - 1):
        if valid_entry[index] == valid_entry[index + 1]:
            valid_entry[index] *= 2
            valid_entry.pop(index + 1)
        if len(valid_entry) - index <= 2:
            break
    zero_num = len(line) - len(valid_entry)
    return valid_entry + [0] * zero_num


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_tiles = {UP:[], DOWN:[], LEFT:[], RIGHT:[]}
        for row in range(self._grid_height):
            self._initial_tiles[LEFT].append((row, 0))
            self._initial_tiles[RIGHT].append((row, self._grid_width - 1))
        for col in range(self._grid_width):
            self._initial_tiles[UP].append((0, col))
            self._initial_tiles[DOWN].append((self._grid_height - 1, col))

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [ [0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        board = ''
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                board += str(self._grid[row][col])
            board += "\n"
        return board

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        for tiles in self._initial_tiles[direction]:
            row = tiles[0]
            col = tiles[1]
            value_list = []
            print str(self)
            while (row in range(self._grid_height)) and (col in range(self._grid_width)):
                value_list.append(self._grid[row][col])
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            value_merged = merge(value_list)
            if value_merged != value_list:
                moved = True
            while row != tiles[0] or col != tiles[1]:
                row -= OFFSETS[direction][0]
                col -= OFFSETS[direction][1]
                self.set_tile(row, col, value_merged.pop())
        if moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zero_tiles = []
        initial_numbers = [2] * 9 + [4]
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self.get_tile(row, col) == 0:
                    zero_tiles.append([row, col])
        if zero_tiles != []:
            tile_value = random.choice(initial_numbers)
            tile_select = random.choice(zero_tiles)
            self.set_tile(tile_select[0], tile_select[1], tile_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

#trial = TwentyFortyEight(5, 4)
#print str(trial)
#trial.set_tile(4, 3, 8)
#print str(trial)

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
