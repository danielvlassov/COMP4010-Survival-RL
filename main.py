import numpy as np
from agents.dqn import DQN_Agent
from environment.grid_world import GridWorld
from config import ENV_CONFIG as config
from agents.random_agent import RandomAgent

def main():
    grid_world = GridWorld(config, 'island-map')
    agent_initial_state = {
        'position': [0, 0],
        'inventory': config['initial_inventory'],
        'hunger_level': 100
    }

    random_agent = RandomAgent(agent_initial_state, config, grid_world)

    total_reward = 0
    with open('simulation_output.txt', 'w') as output_file:
        output_file.write("Initial World\n")
        output_file.write(grid_world.render())
        step = 1;
        while random_agent.hunger_level > 0:
            action = random_agent.choose_action()
            if action:
                output_file.write(f"Step {step}: Agent performs action: {action}\n")
                random_agent.perform_action(action)
                reward = random_agent.calculate_reward(action)
                total_reward += reward
                output_file.write(f"Reward for action: {reward}\n")
                output_file.write(f"Agent inventory is: {random_agent.inventory}\n")
            else:
                output_file.write("No valid actions available. Ending simulation.\n")
                break
            output_file.write(grid_world.render())
            step += 1;

        output_file.write(f"TOTAL REWARD: {total_reward}\n")


def train_dqn(env, episodes=1000):
    state_size = env.state_size
    action_size = env.action_size
    agent = DQN_Agent(state_size, action_size)
    
    for episode in range(episodes):
        env._current_cell = (0, 0)  # Reset agent to start position
        state = env._to_state[env._current_cell]
        state = np.reshape(state, [1, state_size])
        total_reward = 0

        for t in range(100):  # Limit steps per episode
            action = agent.act(state)
            next_state, reward = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, False)
            state = next_state
            total_reward += reward

            if len(agent.memory) > agent.batch_size:
                agent.replay()

            # Stop episode if agent reaches water or dies (customize this condition)
            x, y = env._current_cell
            if env.grid[y, x] == 'W' or reward == ENV_CONFIG['agent_rewards']['dies']:
                if reward == ENV_CONFIG['agent_rewards']['dies']:
                    print("Agent died!")
                break

        agent.update_target_model()
        print(f"Episode {episode + 1}: Total reward = {total_reward}")

        if episode % 10 == 0:
            agent.save(f"dqn_model_{episode}.npy")

def test_dqn(env):
    state_size = env.state_size
    action_size = env.action_size
    agent = DQN_Agent(state_size, action_size)
    agent.load("dqn_model_final.npy")  # Load the trained model

    env._current_cell = (0, 0)  # Reset agent to start position
    state = env._to_state[env._current_cell]
    state = np.reshape(state, [1, state_size])
    steps = 0

    while steps < 100:  # Limit steps per test
        q_values = agent._forward(state, agent.model)
        action = np.argmax(q_values)  # Always take the best action
        next_state, reward = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        state = next_state
        steps += 1

        x, y = env._current_cell
        if env.grid[y, x] == 'W':
            print("Agent reached the water! Goal achieved!")
            break

if __name__ == "__main__":
    #main()
    env = GridWorld(config, 'island-map')
    train_dqn(env)
    test_dqn(env)
