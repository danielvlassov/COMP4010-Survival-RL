#TODO: IMPLEMENT GRID WORLDS
import numpy as np
from environment.resources import Berry, Wood, Animal
from agent import Agent

class GridWorld:
    def __init__(self, config):
        self.grid_size = config['grid_size']
        self.grid = self._initialize_grid()
        self.agents = []
        self.resources = []
        self.setup_resources(config)
    
    def _initialize_grid(self):
        # Create a blank grid with specified size
        return np.zeros(self.grid_size)
    
    def setup_resources(self, config):
        # Place berries, wood, and animals based on config
        pass
    
    def step(self, agent_actions):
        # Update the environment based on agents' actions
        pass
    
    def render(self):
        # Display the grid (CLI or graphical)
        pass
