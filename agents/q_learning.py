#TODO: Q-LEARNING IMPLEMENTATION 
# from rl_agent import RL_Agent
import numpy as np
# from scipy.spatial.distance import cdist
# use action masking to limit some actions (a = argmax(Q(s)))

# class QLearning_Agent(RL_Agent):

def QLearning(env, gamma=0.99, step_size=0.1, epsilon=0.1, max_episode=2000, evaluate_every=20):
    # max it will hold is (not possible)
    # 9 * 10 * 10 * 100 * 100 * 100
    Q = {}
    def e_greedy(env, e, s):
        if np.random.rand() < e:
            return np.random.choice(env.n_actions)
        else:
            q_vals = []
            a = env.n_actions
            # print(a)
            for i in range(env.n_actions):
                q_vals.append(get_q(s, i))
            return np.argmax(q_vals)
    def get_q(s, a) :
        if (s, a) not in Q:
            Q[(s, a)] = 0
        return Q[(s, a)]
    
    total_rewards = []
    for i in range(1, max_episode + 1):
        state, _ = env.reset()
        # return
        terminated = False
        curr_reward = 0
        while not terminated:
            action = e_greedy(env, epsilon, state)

            # action = 1
            next_state, reward, terminated, _, _ = env.step(action)
            # print(reward)
            curr_reward += reward

            q_vals = []
            for j in range(env.n_actions):
                q_vals.append(get_q(next_state, j))

            next_action = np.argmax(q_vals)
            Q[(state, action)] += step_size * (reward + gamma * get_q(next_state, next_action) - get_q(state, action))
            state = next_state
        # print(i ,curr_reward)
        if i % evaluate_every == 0:
            total_rewards.append(curr_reward)

    return total_rewards, Q