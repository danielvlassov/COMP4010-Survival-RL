#TODO: IMPLEMENT GRID WORLDS
import numpy as np
import random
from environment.resources import Berry, Wood, Animal

class GridWorld:
    def __init__(self, config, map_layout):
        self.grid_size = config['grid_size']
        self.berry_spawn_rate = config['berry_spawn_rate']
        self.wood_spawn_rate = config['wood_spawn_rate']
        self.deer_spawn_rate = config['animal_spawn_rate']
        self.hunger_decay_rate = config['hunger_decay_rate']
        self.grid = self._initialize_grid_from_string(config, map_layout)
        self.agents = []
        self.resources = []
        self.setup_resources()
    
    def _initialize_grid_from_string(self, config, map_string):
        map_lines = [line.strip() for line in config[map_string].strip().split('\n')]
        
        grid = np.array([list(line) for line in map_lines], dtype=object)

        return grid

    def setup_resources(self):
        for y in range(self.grid_size[0]):
            for x in range(self.grid_size[1]):
                if self.grid[y, x] == 'L':
                    if random.random() < self.berry_spawn_rate:
                        self.resources.append(Berry((x, y)))
                    elif random.random() < self.wood_spawn_rate:
                        self.resources.append(Wood((x, y)))
                    elif random.random() < self.deer_spawn_rate:
                        self.resources.append(Animal((x, y)))
    
    def render(self):
        for y in range(self.grid_size[0]):
            row = ''
            for x in range(self.grid_size[1]):
                resource = self.get_resource_at(x, y)
                if resource:
                    row += resource.symbol
                else:
                    row += '.' if self.grid[y, x] == 'L' else '~'
            print(row)
        print()

    def get_resource_at(self, x, y):
        for resource in self.resources:
            if resource.position[0] == x and resource.position[1] == y:
                return resource
        return None

    def get_block_type_at(self, x, y):
        return self.grid[y, x]