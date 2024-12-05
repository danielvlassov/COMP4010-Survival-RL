from agents.rl_agent import RL_Agent
import numpy as np
import random
from collections import deque

class DQN_Agent(RL_Agent):
    def __init__(self, state_size, action_size, gamma=0.95, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, learning_rate=0.001, batch_size=64, memory_size=2000):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma  # discount rate
        self.epsilon = epsilon  # exploration rate
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = {
            'W1': np.random.randn(self.state_size, 24) * 0.01,
            'b1': np.zeros((1, 24)),
            'W2': np.random.randn(24, 24) * 0.01,
            'b2': np.zeros((1, 24)),
            'W3': np.random.randn(24, self.action_size) * 0.01,
            'b3': np.zeros((1, self.action_size))
        }
        return model

    def update_target_model(self):
        self.target_model = {k: v.copy() for k, v in self.model.items()}

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self._forward(state, self.model)
        return np.argmax(q_values)

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self._forward(state, self.model)
            if done:
                target[0][action] = reward
            else:
                t = self._forward(next_state, self.target_model)
                target[0][action] = reward + self.gamma * np.amax(t)
            self._train(state, target)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def _forward(self, state, model):
        z1 = np.dot(state, model['W1']) + model['b1']
        a1 = np.maximum(0, z1)  # ReLU activation
        z2 = np.dot(a1, model['W2']) + model['b2']
        a2 = np.maximum(0, z2)  # ReLU activation
        z3 = np.dot(a2, model['W3']) + model['b3']
        return z3  # Linear activation

    def _train(self, state, target):
        # Forward pass
        z1 = np.dot(state, self.model['W1']) + self.model['b1']
        a1 = np.maximum(0, z1)  # ReLU activation
        z2 = np.dot(a1, self.model['W2']) + self.model['b2']
        a2 = np.maximum(0, z2)  # ReLU activation
        z3 = np.dot(a2, self.model['W3']) + self.model['b3']

        # Compute loss (Mean Squared Error)
        loss = np.mean((z3 - target) ** 2)

        # Backward pass
        dz3 = z3 - target
        dW3 = np.dot(a2.T, dz3)
        db3 = np.sum(dz3, axis=0, keepdims=True)

        da2 = np.dot(dz3, self.model['W3'].T)
        dz2 = da2 * (a2 > 0)
        dW2 = np.dot(a1.T, dz2)
        db2 = np.sum(dz2, axis=0, keepdims=True)

        da1 = np.dot(dz2, self.model['W2'].T)
        dz1 = da1 * (a1 > 0)
        dW1 = np.dot(state.T, dz1)
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # Update weights
        self.model['W1'] -= self.learning_rate * dW1
        self.model['b1'] -= self.learning_rate * db1
        self.model['W2'] -= self.learning_rate * dW2
        self.model['b2'] -= self.learning_rate * db2
        self.model['W3'] -= self.learning_rate * dW3
        self.model['b3'] -= self.learning_rate * db3

    def load(self, name):
        self.model = np.load(name, allow_pickle=True).item()

    def save(self, name):
        np.save(name, self.model)