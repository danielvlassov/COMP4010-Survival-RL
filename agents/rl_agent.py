#BASE REINFORCEMENT LEARNING AGENT
from config import ENV_CONFIG
from environment.agent import Agent 

class RL_Agent(Agent):
    def __init__(self, initial_state, config, env):
        super().__init__(initial_state, config, env)
        self.visited_cells = set()
        env.agents.append(self)

    def get_state(self):
        position = (self.position[0], self.position[1])
        inventory = (self.inventory.get('berry', 0), self.inventory.get('wood', 0))
        hunger = self.hunger_level
        return (position, inventory, hunger)

    def get_valid_actions(self):
        valid_actions = []

        for direction in ['up', 'down', 'left', 'right']:
            new_x, new_y = self._calculate_new_position(direction)
            if self._is_valid_move(new_x, new_y, direction):
                valid_actions.append(direction)

        resource = self.env.get_resource_at(self.position[0], self.position[1])
        if resource and resource.symbol != 'A':
            valid_actions.append(f"pick_up_{resource.type}")

        if self.inventory.get('wood', 0) >= 3:
            valid_actions.append('build_boat')
        if self.inventory.get('wood', 0) >= 2:
            valid_actions.append('build_sword')

        if self.inventory['sword'] > 0 and resource and resource.symbol == 'A':
            valid_actions.append('hunt')

        return valid_actions

    def calculate_reward(self, action):
        if action.startswith('pick_up'):
            resource_name = action.split('_')[-1]
            if resource_name == 'berry':
                return ENV_CONFIG['agent_rewards']['pick_up_berry']
            elif resource_name == 'wood':
                return ENV_CONFIG['agent_rewards']['pick_up_wood']
        
        elif action == 'build_boat':
            return ENV_CONFIG['agent_rewards']['build_boat']
        
        elif action == 'build_sword':
            return ENV_CONFIG['agent_rewards']['build_sword']
        
        elif action == 'hunt':
            return ENV_CONFIG['agent_rewards']['hunt_animal']
        
        elif action in ['up', 'down', 'left', 'right']:
            current_position = (self.position[0], self.position[1])
            if current_position not in self.visited_cells:
                self.visited_cells.add(current_position)
                return ENV_CONFIG['agent_rewards']['explore_new_cell']
        
        elif self.hunger_level <= 0:
            return ENV_CONFIG['agent_rewards']['dies'] 
        
        return 0

    def _calculate_new_position(self, direction):
        new_x, new_y = self.position
        if direction == 'up':
            new_y -= 1
        elif direction == 'down':
            new_y += 1
        elif direction == 'left':
            new_x -= 1
        elif direction == 'right':
            new_x += 1
        return new_x, new_y

    def _is_valid_move(self, x, y, direction):
        if not (0 <= x < self.env.grid_size[1] and 0 <= y < self.env.grid_size[0]):
            return False
        
        if self.env.get_block_type_at(x, y) == 'W' and self.inventory['boat'] == 0:
            return False
        
        if self.env.get_block_type_at(x, y) == 'W':
            return self._check_water_move(x, y, direction)
        
        return True

    def perform_action(self, action):
        if action in ['up', 'down', 'left', 'right']:
            self.move(action)
            

        elif action.startswith('pick_up'):
            resource_name = action.split('_')[-1]
            self.pick_up(resource_name, self.position[0], self.position[1])

        elif action == 'build_boat' and self.inventory['wood'] >= 3:
            self.build('boat')

        elif action == 'build_sword' and self.inventory['wood'] >= 2:
           self.build('sword')

        elif action == 'hunt':
            self.hunt(self.position[0],  self.position[1])

        self.hunger_level -= 1

        if self.hunger_level <= 0:
            return "Agent has died of hunger."
            return False

        return True

    def _check_water_move(self, x, y, direction):
        grid_size = self.env.grid_size
        while 0 <= x < grid_size[1] and 0 <= y < grid_size[0]:
            block_type = self.env.get_block_type_at(x, y)
            if block_type == 'L':
                return True
            if direction == 'up':
                y -= 1
            elif direction == 'down':
                y += 1
            elif direction == 'left':
                x -= 1
            elif direction == 'right':
                x += 1

        return False
