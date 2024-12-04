import random
from agents.rl_agent import RL_Agent

class RandomAgent(RL_Agent):
    def __init__(self, initial_state, config, env):
        super().__init__(initial_state, config, env)

    def choose_action(self):
        valid_actions = self.get_valid_actions()
        if valid_actions:
            return random.choice(valid_actions)
        return None
    