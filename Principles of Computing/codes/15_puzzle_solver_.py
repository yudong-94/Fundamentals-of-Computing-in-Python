# http://www.codeskulptor.org/#user41_DFa09EqEAJvMQSv.py

"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

DOWNWARD_RIGHT = 'rddlu'
DOWNWARD_LEFT = 'lddru'
LEFTWARD_DOWN = 'dllur'
LEFTWARD_UP = 'ulldr'
RIGHTWARD_DOWN = 'druldru'
RIGHTWARD_UP = 'urrdl'


import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.current_position(0, 0) != (target_row, target_col):
            print '0 tile not at the position specified'
            return False
        for row in range(target_row + 1, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    print 'lower rows not satisify the solved position'
                    return False
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(target_row, col) != (target_row, col):
                print 'right tiles at the target row not satisfy the solved position'
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        #assert self.lower_row_invariant(self, target_row, target_col), "incorrect interior_tile input"
        current_pos = self.current_position(target_row, target_col)
        if current_pos[0] == target_row:
            #print "case 1"
            # target tile locates at the left part of the row
            # move 0 tile to the current position of target tile
            solve_string = "l" * (target_col - current_pos[1])
            # move target tile to right one by one step
            solve_string += "urdruldruld" * (target_col - current_pos[1] - 1)
            #print solve_string
        elif current_pos[1] == target_col:
            #print "case 2"
            # target tile locates right up the 0 tile
            # move 0 tile to the current position of target tile
            solve_string = "u" * (target_row - current_pos[0])
            # move target tile down one by one step
            solve_string += DOWNWARD_LEFT * (target_row - current_pos[0] - 1)
            # move 0 tile to the left of the target tile
            solve_string += "ld"
            #print solve_string
        elif current_pos[1] < target_col:
            #print "case 3"
            # target tile locates on the upper left part
            # move 0 tile to the current position of target tile
            solve_string = "l" * (target_col - current_pos[1]) + "u" * (target_row - current_pos[0])
            # move target tile down one by one step
            solve_string += DOWNWARD_RIGHT * (target_row - current_pos[0] - 1)
            # move target tile right one by one step
            solve_string += RIGHTWARD_DOWN * (target_col - current_pos[1])
            solve_string += "ld"
            #print solve_string
        else:
            #print "case 4"
            # target tile locates on the upper right part
            # move 0 tile to the current position of target tile
            solve_string = "u" * (target_row - current_pos[0]) + "r" * (current_pos[1] - target_col)
            # move target tile left one by one step
            solve_string += LEFTWARD_UP * (current_pos[1] - target_col - 1)
            # move 0 tile to the up position of the target tile
            solve_string += "dlu"
            # move target tile down one by one step
            solve_string += DOWNWARD_LEFT * (target_row - current_pos[0] - 1)
            solve_string += "ld"
            #print solve_string
        self.update_puzzle(solve_string)
        #assert self.lower_row_invariant(self, target_row, target_col - 1), "incorrect solve_interior_tile"
        return solve_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        #assert self.lower_row_invariant(target_row, 0), "incorrect col0_tile input"
        current_pos = self.current_position(target_row, 0)
        # move 0 tile to the position of the target tile (X0)
        solve_string = "u" * (target_row - current_pos[0]) + "r" * current_pos[1]
        if current_pos[1] == 0 and (target_row - current_pos[0]) > 1:
            # move target tile downward to the position (i-1, 0)
            solve_string += DOWNWARD_RIGHT * (target_row - current_pos[0] - 2)
            # move target tile to (i-1, 1), and o tile to (i-1, 0)
            solve_string += "rdl"
            # move target tile using a 3X2 solution
            solve_string += "ruldrdlurdluurddlur"
            # move 0 tile to column n
            solve_string += "r" * (self.get_width() - 2)
        elif current_pos[1] == 0 and (target_row - current_pos[0]) == 1:
            # target tile has been in the correct position, move 0 tile to column n
            solve_string += "r" * (self.get_width() - 1)
        elif current_pos[1] > 0:
            # move target tile leftward to the column 0 (X0)
            solve_string += LEFTWARD_DOWN * (current_pos[1] - 1)
            # move 0 tile to the up position of the target tile (0|X)
            if current_pos[0] == 0:
                solve_string += "dlu"
                # move tile downward
                solve_string += DOWNWARD_RIGHT * (target_row - current_pos[0] - 2)
            else:
                solve_string += "ul"
                # move target tile downward to the row i-1 (0|X)
                solve_string += DOWNWARD_RIGHT * (target_row - current_pos[0] - 1)
            # move 0 tile to the left position of the target tile (0X)
            solve_string += "rdl"
            # move target tile using a 3X2 solution
            solve_string += "ruldrdlurdluurddlur"
            # move 0 tile to column n
            solve_string += "r" * (self.get_width() - 2)
        #print solve_string
        self.update_puzzle(solve_string)
        #assert self.lower_row_invariant(target_row-1, self.get_width()-1), "incorrect col0_tile solver"
        return solve_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.current_position(0, 0) != (0, target_col):
            return False
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    print 'lower rows not satisify the solved position'
                    return False
        for col in range(target_col, self.get_width()):
            if self.current_position(1, col) != (1, col):
                print 'right tiles at the row 1 not satisfy the solved position'
                return False
        for col in range(target_col+1, self.get_width()):
            if self.current_position(1, col) != (1, col):
                print 'right tiles at the row 0 not satisfy the solved position'
                return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.current_position(0, 0) != (1, target_col):
            return False
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    print 'lower rows not satisify the solved position'
                    return False
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(1, col) != (1, col) or self.current_position(0, col) != (0, col):
                print 'right tiles at the target row not satisfy the solved position'
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        # move 0 tile to (1, j-1)
        self.update_puzzle("ld")
        current_pos = self.current_position(0, target_col)
        if current_pos == (0, target_col):
            solve_string = ""
        else:
            if current_pos[0] == 1:
                solve_string = "l" * (target_col - current_pos[1] - 1)
                solve_string += RIGHTWARD_UP * ((target_col - current_pos[1] - 2))
            elif current_pos[1] == target_col - 1:
                solve_string = "uld"
            else:
                solve_string = "l" * (target_col - current_pos[1] - 1) + "u"
                solve_string += "rdl"
                solve_string += RIGHTWARD_UP * ((target_col - current_pos[1] - 2))
            solve_string += "urdlurrdluldrruld"
        #print solve_string
        self.update_puzzle(solve_string)
        assert self.row1_invariant(target_col - 1)
        return "ld"+solve_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "input error"
        current_pos = self.current_position(1, target_col)
        # move to the position of target tile (0|X)
        solve_string = "l" * (target_col - current_pos[1]) + "u" * (1 - current_pos[0])
        if current_pos[0] == 0:
            solve_string += "rdlur" * (target_col - current_pos[1])
        else:
            solve_string += RIGHTWARD_UP * (target_col - current_pos[1] - 1)
            solve_string += "ur"

        #print solve_string
        self.update_puzzle(solve_string)
        assert self.row0_invariant(target_col), "solver error"
        return solve_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1), "incorrect input"
        if self.current_position(0, 1) == (0, 0):
            #current: 15|40
            solve_string = "ul"
        if self.current_position(0, 1) == (0, 1):
            #current: 41|50
            solve_string = "lurdlurdlurdlu"
        if self.current_position(0, 1) == (1, 0):
            #current: 54|10
            solve_string = "uldrul"
        self.update_puzzle(solve_string)
        return solve_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        solve_string = ""
        current_pos = self.current_position(0, 0)
        solve_string += "d" * (self.get_height() - 1 - current_pos[0]) + "r" * (self.get_width() - 1 - current_pos[1])
        self.update_puzzle(solve_string)
        print self
        current_pos = self.current_position(0, 0)
        for row in range(self.get_height()-1, 1, -1):
            for col in range(self.get_width()-1, 0, -1):
                solve_string += self.solve_interior_tile(row, col)
                print (row, col)
                print self
            solve_string += self.solve_col0_tile(row)
        print self
        for col in range(self.get_width()-1, 1, -1):
            solve_string += self.solve_row1_tile(col)
            solve_string += self.solve_row0_tile(col)
        solve_string += self.solve_2x2()
        return solve_string


# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4,[[4, 2, 3, 7],[8, 5, 1, 11],[12, 9, 6, 10],[13, 14, 15, 0]]))

# test sample
#test = Puzzle(4, 4,[[4, 2, 3, 7],[8, 5, 1, 11],[12, 9, 6, 10],[13, 14, 15, 0]])
#print test
#test.solve_row0_tile(2)
#print test

#test = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print test
#test.solve_puzzle()
#print test
