import random
import copy 

class Grid:
    def __init__(self, x_axel_length, y_axel_length):
        self.x_axel_length = x_axel_length
        self.y_axel_length = y_axel_length

        self.grid = []
        self.grid_history = []

    def get_grid(self, x_pos, y_pos):
        val = self.grid[x_pos][y_pos]
        return val
    
    def set_grid(self, x_pos, y_pos, value):
        self.grid[x_pos][y_pos] = value

    def getRandint(self, min, max):
        return random.randint(min,max)
    
    def initialize(self):
        for x_axel in range(0, self.x_axel_length):
            filler = []
            for y_axel in range(0, self.y_axel_length):
                filler.append(0)
            self.grid.append(filler)
            
    def getRandomEmptyLocation(self):
        x_pos = self.getRandint(0, self.x_axel_length - 1) 
        y_pos = self.getRandint(0, self.y_axel_length - 1) 
        if (self.get_grid(x_pos, y_pos) == 0):
            return [x_pos, y_pos]
        else:
            empty_position_found = False
            while not empty_position_found:
                x_pos = self.getRandint(0, self.x_axel_length - 1) 
                y_pos = self.getRandint(0, self.y_axel_length - 1) 
                if (self.get_grid(x_pos, y_pos) == 0):
                    empty_position_found = True
                    return [x_pos, y_pos]

    def placeValueInRandomLocation(self, instances, value):
        for instance in range(0, instances):
            x_pos = self.getRandint(0, self.x_axel_length - 1) 
            y_pos = self.getRandint(0, self.y_axel_length - 1) 
            if (self.get_grid(x_pos, y_pos) == 0):
                self.set_grid(x_pos, y_pos, value)
            else:
                empty_position_found = False
                while not empty_position_found:
                    x_pos = self.getRandint(0, self.x_axel_length - 1) 
                    y_pos = self.getRandint(0, self.y_axel_length - 1) 
                    if (self.get_grid(x_pos, y_pos) == 0):
                        self.set_grid(x_pos, y_pos, value)
                        empty_position_found = True

    def getValueLocations(self, value):
        locations = []
        for x_coord in range(0, self.x_axel_length):
            for y_coord in range(0, self.y_axel_length):
                if(self.get_grid(x_coord, y_coord) == value): 
                    locations.append([x_coord, y_coord])
        return locations
    
    def checkIfValueCloseToLocation(self, x_coord, y_coord, value):
        value_found = False
        min_x_coord = max(0, x_coord - 1)
        min_y_coord = max(0, y_coord - 1)
        max_x_coord = min(self.x_axel_length - 1, x_coord + 1)
        max_y_coord = min(self.y_axel_length - 1, y_coord + 1)

        for x_pos in range(min_x_coord, max_x_coord + 1):
            for y_pos in range(min_y_coord, max_y_coord + 1):
                if(self.get_grid(x_pos, y_pos) == value):
                    if not(x_pos == x_coord and y_pos == y_coord):
                        value_found = True
                    
        return value_found

    def getLocationWithValueCloseToLocation(self, x_coord, y_coord, value):
        possible_x_positions = [x for x in range(max(0, x_coord - 1), min(self.x_axel_length, x_coord + 2))]
        possible_y_positions = [y for y in range(max(0, y_coord - 1), min(self.y_axel_length, y_coord + 2))]

        random.shuffle(possible_x_positions)
        random.shuffle(possible_y_positions)

        for x_pos in possible_x_positions:
            for y_pos in possible_y_positions:
                if(self.get_grid(x_pos, y_pos) == value):
                    return [x_pos, y_pos]
        return None
    
    
    
    def saveGridHistory(self):
        copyofgrid = copy.deepcopy(self.grid)
        self.grid_history.append(copyofgrid)
