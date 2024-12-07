from environment.grid_world import GridWorld
from config import ENV_CONFIG as config
from agents.random_agent import RandomAgent
from agents.q_learning import QLearning

def main():
    grid_world = GridWorld(config, 'island-map')
    agent_initial_state = {
        'position': [2, 0],
        'inventory': config['initial_inventory'],
        'hunger_level': 100
    }
    rewards, Q = QLearning(grid_world)
    # QLearning(grid_world)
    for q in Q:
        print(q, Q[q])
    # print(Q)
    print(rewards)

    # random_agent = RandomAgent(agent_initial_state, config, grid_world)

    # total_reward = 0
    # with open('simulation_output.txt', 'w') as output_file:
    #     output_file.write("Initial World\n")
    #     output_file.write(grid_world.render())
    #     step = 1;
    #     while random_agent.hunger_level > 0:
    #         action = random_agent.choose_action()
    #         if action:
    #             output_file.write(f"Step {step}: Agent performs action: {action}\n")
    #             random_agent.perform_action(action)
    #             reward = random_agent.calculate_reward(action)
    #             total_reward += reward
    #             output_file.write(f"Reward for action: {reward}\n")
    #             output_file.write(f"Agent inventory is: {random_agent.inventory}\n")
    #         else:
    #             output_file.write("No valid actions available. Ending simulation.\n")
    #             break
    #         output_file.write(grid_world.render())
    #         step += 1;

    #     output_file.write(f"TOTAL REWARD: {total_reward}\n")

if __name__ == "__main__":
    main()
