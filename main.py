from environment.grid_world import GridWorld
from config import ENV_CONFIG as config
def main():
    grid_world = GridWorld(config, 'island-map')
    grid_world.render()

if __name__ == "__main__":
    main()