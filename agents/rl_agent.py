#BASE REINFORCEMENT LEARNING AGENT
from config import ENV_CONFIG
from environment.agent import Agent 

class RL_Agent(Agent):
    def __init__(self, initial_state, config, env):
        super().__init__(initial_state, config, env)  

    def get_state(self):
        position = (self.position[0], self.position[1])
        inventory = (self.inventory.get('berry', 0), self.inventory.get('wood', 0))
        tools = (self.tools['boat'], self.tools['sword'])
        hunger = self.hunger_level
        return (position, inventory, tools, hunger)

    def get_valid_actions(self):
        valid_actions = []

        for direction in ['up', 'down', 'left', 'right']:
            new_x, new_y = self._calculate_new_position(direction)
            if self._is_valid_move(new_x, new_y):
                valid_actions.append(direction)

        resource = self.env.get_resource_at(self.position[0], self.position[1])
        if resource:
            valid_actions.append(f"pick_up_{resource.symbol}")  # Example: 'pick_up_berry'

        if self.inventory.get('wood', 0) >= 3 and not self.tools['boat']:
            valid_actions.append('build_boat')
        if self.inventory.get('wood', 0) >= 2 and not self.tools['sword']:
            valid_actions.append('build_sword')

        if self.tools['sword'] and resource and resource.symbol == 'A':  # Assuming 'A' stands for animal
            valid_actions.append('hunt')

        return valid_actions

    def calculate_reward(self, action):
        if action.startswith('pick_up'):
            resource_type = action.split('_')[-1]
            if resource_type == 'berry':
                return ENV_CONFIG['agent_rewards']['collecting_berry']
            elif resource_type == 'wood':
                return ENV_CONFIG['agent_rewards']['collecting_wood']
        
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
            new_y += 1
        elif direction == 'down':
            new_y -= 1
        elif direction == 'left':
            new_x -= 1
        elif direction == 'right':
            new_x += 1
        return new_x, new_y

    def _is_valid_move(self, x, y):
        if not (0 <= x < self.env.grid_size[1] and 0 <= y < self.env.grid_size[0]):
            return False
        
        if self.env.get_block_type_at(x, y) == 'Water' and not self.tools['boat']:
            return False
        
        return True

