# Configuration for the environment and agent
ENV_CONFIG = {
    'grid_size': (10, 10),          # Dimensions of the grid
    'berry_spawn_rate': 0.1,        # Chance of berry spawning on each tile
    'wood_spawn_rate': 0.05,        # Chance of wood appearing on forest tiles
    'animal_count': 5,              # Number of animals in the environment
    'hunger_decay_rate': 0.01,      # Hunger level decay per time step
    'initial_resources': {
        'wood': 0,
        'berries': 0,
        'boats': 0,
        'swords': 0
    },
    # Agent-related configurations
    'agent_params': {
        'learning_rate': 0.1,
        'discount_factor': 0.99,
        'epsilon': 0.1,             
    }
}
