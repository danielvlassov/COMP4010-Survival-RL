#TODO: BASE AGENT PROPERTIES AND ACTIONS

from config import ENV_CONFIG 
class Agent:
    def __init__(self, initial_state, config, env):
        self.position = initial_state['position']
        self.inventory = config['initial_resources']
        self.hunger_level = 100
        self.tools = {'boat': False, 'sword': False}
        self.env = env

    def move(self, direction):
        if direction == 'up':
            self.position[1] += 1
        elif direction == 'down':
            self.position[1] -= 1
        elif direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1
        else:
            print("Invalid direction")
        
        #MOVE LOGIC UP TO ALL IMPLEMENTATION WHENEVER ACTION IS TAKEM 
        # self.hunger_level -= ENV_CONFIG.hunger_decay_rate
        # if self.hunger_level <= 0:
        #     print("Agent is starving!")

    def pick_up(self, resource, env):
        if resource in self.inventory:
            self.inventory[resource] += 1
        else:
            self.inventory[resource] = 1

        if resource == 'berry':
            self.hunger_level = min(100, self.hunger_level + 5)
            print(f"Ate a berry. Hunger level is now {self.hunger_level}.")
        self.env.resources.remove(resource)

    def build(self, item):
        if item == 'boat':
            if self.inventory.get('wood', 0) >= 3:
                self.tools['boat'] = True
                self.inventory['wood'] -= 3
                print("Built a boat!")
            else:
                print("Not enough wood to build a boat.")
        
        elif item == 'sword':
            if self.inventory.get('wood', 0) >= 2:
                self.tools['sword'] = True
                self.inventory['wood'] -= 2
                print("Built a sword!")
            else:
                print("Not enough resources to build a sword.")
        else:
            print(f"Cannot build {item}. Only 'boat' or 'sword' are buildable.")

    def hunt(self):
        if not self.tools['sword']:
            print("You need a sword to hunt!")
            return
        self.env.resources.remove(self.env.get_resource_at(self.position[0], self.position[1]))
        self.hunger_level = min(100, self.hunger_level + 20)
        print(f"Hunger level after hunting: {self.hunger_level}")
