"""
Student portion of Zombie Apocalypse mini-project
"""

# http://www.codeskulptor.org/#user41_YDI9CQ6tyOz5hZj.py

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        #for row in range(self.get_grid_height()):
        #    for col in range(self.get_grid_width()):
        #        self.set_empty(row, col)


    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        visited.clear()
        distance_field = [[self.get_grid_height()*self.get_grid_width() for dummy_col in range(self.get_grid_width())]
                       for dummy_row in range(self.get_grid_height())]
        #print distance_field
        boundary = poc_queue.Queue()
        entity_func = {ZOMBIE:self.zombies(), HUMAN:self.humans()}
        #print entity_type
        for entity in entity_func[entity_type]:
            #print entity
            boundary.enqueue(entity)
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0
        #print distance_field
        while len(boundary)!=0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for cell in neighbors:
                if visited.is_empty(cell[0], cell[1]) and self.is_empty(cell[0], cell[1]):
                    visited.set_full(cell[0], cell[1])
                    boundary.enqueue(cell)
                    distance_field[cell[0]][cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for human in self.humans():
            neighbors = self.eight_neighbors(human[0], human[1])
            max_distance = zombie_distance_field[human[0]][human[1]]
            top_cells = [human]
            for cell in neighbors:
                if self.is_empty(cell[0], cell[1]):
                    if max_distance < zombie_distance_field[cell[0]][cell[1]]:
                        max_distance = zombie_distance_field[cell[0]][cell[1]]
                        top_cells = [cell]
                    elif max_distance == zombie_distance_field[cell[0]][cell[1]]:
                        top_cells.append(cell)
            top_choice = random.choice(top_cells)
            new_human_list.append(top_choice)
        self._human_list = new_human_list

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        for zombie in self.zombies():
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            min_distance = human_distance_field[zombie[0]][zombie[1]]
            top_cells = [zombie]
            for cell in neighbors:
                if self.is_empty(cell[0], cell[1]):
                    if min_distance > human_distance_field[cell[0]][cell[1]]:
                        min_distance = human_distance_field[cell[0]][cell[1]]
                        top_cells = [cell]
                    elif min_distance == human_distance_field[cell[0]][cell[1]]:
                        top_cells.append(cell)
            top_choice = random.choice(top_cells)
            new_zombie_list.append(top_choice)
        self._zombie_list = new_zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))



#test = Apocalypse(3, 4, obstacle_list=[(1, 1)], zombie_list=[(2, 2), (2, 3)])
#print test
#test.clear()
#print test
#test.add_zombie(0, 0)
#print test._zombie_list
#print test.compute_distance_field(ZOMBIE)
