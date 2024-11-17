#TODO: BASE AGENT PROPERTIES AND ACTIONS
class Agent:
    def __init__(self, initial_state, config):
        self.position = initial_state['position']
        self.inventory = config['initial_resources']
        self.hunger_level = 100
        self.tools = {'boat': False, 'sword': False}
    
    def move(self, direction):
        # Logic for agent movement
        pass
    
    def pick_up(self, resource):
        # Logic for picking up resources
        pass
    
    def build(self, item):
        # Build boat or sword based on inventory
        pass
    
    def hunt(self, animal):
        # Hunt an animal if holding a sword
        pass
