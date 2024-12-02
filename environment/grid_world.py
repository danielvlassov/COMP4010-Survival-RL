#TODO: IMPLEMENT GRID WORLDS
import numpy as np
import random
from environment.resources import Berry, Wood, Animal
import gymnasium as gym
from config import ENV_CONFIG


class GridWorld(gym.Env):
    def __init__(self, config, map_layout):
        # movement, with cutting, creating, eating, and placing
        # 0-3 -> movement
        # 4 -> pick up berry
        # 5 -> pick up wood
        # 6 -> make boat
        # 7 -> make sword
        # 8 -> hunt animal
        # will add more later if less lazy (ig cutting works with hunting (check inv))
        # just punish if it makes an invalid move
        self._n_actions = 9
        self._directions = [np.array((-1, 0)), 
                    np.array((1, 0)), 
                    np.array((0, -1)), 
                    np.array((0, 1))]

        # will be [x, y]
        self._current_cell = None

        # state: (x, y, boat, sword)

        self.hunger = 100

        self.grid_size = config['grid_size']

        # state_num = 0
        # self._to_state = {}
        # for i in range(self.grid_size[0]):
        #     for j in range(self.grid_size[1]):
        #         self._to_state[(i, j)] = state_num
        #         state_num += 1

        self.berry_spawn_rate = config['berry_spawn_rate']
        self.wood_spawn_rate = config['wood_spawn_rate']
        self.deer_spawn_rate = config['animal_spawn_rate']
        self.hunger_decay_rate = config['hunger_decay_rate']
        self.grid = self._initialize_grid_from_string(config, map_layout)
        self.agents = []
        self.resources = {}
        # self.resources = []
        self.setup_resources()
    
    def reset(self):
        self.visited_cells = np.zeros((self.grid_size, self.grid_size))
        # self.setup_resources()

        self.wood = 0
        self.boat = 0
        self.sword = 0

        # start on bottom right corner
        x = y = self.grid_size - 1
        state = (x, y, self.wood, self.boat, self.sword) # total states is 10 * 10 * 8???
        return state, {}

    def _initialize_grid_from_string(self, config, map_string):
        map_lines = [line.strip() for line in config[map_string].strip().split('\n')]
        
        grid = np.array([list(line) for line in map_lines], dtype=object)

        return grid

    def setup_resources(self):
        for y in range(self.grid_size[0]):
            for x in range(self.grid_size[1]):
                if self.grid[y, x] == 'L':
                    # if random.random() < self.berry_spawn_rate:
                    #     self.resources.append(Berry((x, y)))
                    # elif random.random() < self.wood_spawn_rate:
                    #     self.resources.append(Wood((x, y)))
                    # elif random.random() < self.deer_spawn_rate:
                    #     self.resources.append(Animal((x, y)))
                    # ???????
                    if random.random() < self.berry_spawn_rate:
                        self.resources[(x, y)] = Berry((x, y))
                    elif random.random() < self.wood_spawn_rate:
                        self.resources[(x, y)] = Wood((x, y))
                    elif random.random() < self.deer_spawn_rate:
                        self.resources[(x, y)] = Animal((x, y))
    
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
        if (x, y) in self.resources:
            return self.resources[(x, y)]
        # for resource in self.resources:
        #     if resource.position[0] == x and resource.position[1] == y:
        #         return resource
        return None

    def get_block_type_at(self, x, y):
        return self.grid[y, x]
    
    def step(self, action):
        self.hunger -= self.hunger_decay_rate
        terminated = self.hunger <= 0

        # move agent
        if action < 4:
            next_blockX, next_blockY = self._current_cell + self._directions[action]
        
        # agent only moves if still within grid
        edgeX, edgeY = self.gridsize
        if 0 <= next_blockX < edgeX and 0 <= next_blockY < edgeY:
            self._current_cell = tuple(next_blockX, next_blockY)
        
        reward = self.calculate_reward(action)

        state = (self._current_cell[0], self._current_cell[1], self.wood, self.boat, self.sword)
        # state = self._to_state[self._current_cell]
        return state, reward, terminated, False, {}
    
    def calculate_reward(self, action):
        reward = -10
        if 0 <= action <= 3:
            x, y = self._current_cell
            # reward if visiting new cell
            if not self.visited_cells[x, y]:
                reward += ENV_CONFIG['agent_rewards']['explore_new_cell']
                self.visited_cells[x, y] = 1
        elif action == 4:
            resource = self.get_resource_at(self._current_cell[0], self._current_cell[1])
            if resource.symbol == "B":
                reward += ENV_CONFIG['agent_rewards']['collecting_berry']
            else:
                reward -= 20 # arbitrary reward for invalid action
        elif action == 5:
            resource = self.get_resource_at(self._current_cell[0], self._current_cell[1])
            if resource.symbol == "W":
                self.wood += 1
                reward += ENV_CONFIG['agent_rewards']['collecting_wood']
            else:
                reward -= 20 # arbitrary reward for invalid action
        elif action == 6:
            # check if they have wood
            self.boat += 1
            reward += ENV_CONFIG['agent_rewards']['build_boat']
        elif action == 7:
            # check if they have wood
            self.sword += 1
            reward += ENV_CONFIG['agent_rewards']['build_sword']
        elif action == 8:
            # check if animal on tile
            # subtract sword 
            reward += ENV_CONFIG['agent_rewards']['hunt_animal']
        
        if self.hunger <= 0:
            reward += ENV_CONFIG['agent_rewards']['dies'] 
        return reward
    
    @property
    def n_actions(self):
        return self.n_actions