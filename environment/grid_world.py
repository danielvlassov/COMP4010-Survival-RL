#TODO: IMPLEMENT GRID WORLDS
import numpy as np
import random
from environment.resources import Berry, Wood, Animal

class GridWorld:
    def __init__(self, config, map_layout):
        # movement, with cutting, creating, eating, and placing
        # 0-3 -> movement
        # 4 -> chop wood
        # 5 -> try to make object
        # 6 -> try to eat
        # 7 -> try to place land
        # will add more later if less lazy (ig cutting works with hunting (check inv))
        # self.n_actions = 8
        self._directions = [np.array((-1, 0)), 
                    np.array((1, 0)), 
                    np.array((0, -1)), 
                    np.array((0, 1))]

        # will be [x, y]
        self._current_cell = None

        self.grid_size = config['grid_size']

        state_num = 0
        self._to_state = {}
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self._to_state[(i, j)] = state_num
                state_num += 1

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
        render_txt = ''
        for y in range(self.grid_size[0]):
            row = ''
            for x in range(self.grid_size[1]):
                agent_at_position = False
                for agent in self.agents:
                    if agent.position == (x, y):
                        row += 'X' 
                        agent_at_position = True
                        break
                if not agent_at_position:
                    resource = self.get_resource_at(x, y)
                    if resource:
                        row += resource.symbol
                    else:
                        row += '.' if self.grid[y, x] == 'L' else '~'
            render_txt += row +  "\n"
        return render_txt

    def get_resource_at(self, x, y):
        for resource in self.resources:
            if resource.position[0] == x and resource.position[1] == y:
                return resource
        return None

    def get_block_type_at(self, x, y):
        return self.grid[y, x]
    
    def step(self, action):
        if action < 4:
            next_blockX, next_blockY = self._current_cell + self._directions[action]
        edgeX, edgeY = self.gridsize
        if 0 <= next_blockX < edgeX and 0 <= next_blockY < edgeY:
            self._current_cell = tuple(next_blockX, next_blockY)
        
        # reward decreases since hp decreases
        reward = -1
        # put reward function here
        # most likely adds if action is craft, or eat

        state = self._to_state[self._current_cell]
        return state, reward

    @property
    def n_actions(self):
        return self.n_actions
    
    def remove_resource_at(self, x, y):
        for resource in self.resources:
            if resource.position == (x, y):
                self.resources.remove(resource)
                self.grid[y, x] = "L"
                return True 
        return False
