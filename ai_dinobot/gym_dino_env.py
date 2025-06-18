# dino_gym_env.py
import gym
from gym import spaces
import numpy as np
from dino_env import DinoGameEnv

class DinoGymEnv(gym.Env):
    def __init__(self):
        super(DinoGymEnv, self).__init__()

        # Initialize your custom game environment
        self.env = DinoGameEnv()

        # Action space: 0 = do nothing, 1 = jump
        self.action_space = spaces.Discrete(2)

        # Observation space: [DINO_Y, y_velocity, distance_to_cactus, cactus_height]
        low = np.array([0, -20, 0, 0, 0], dtype=np.float32)
        high = np.array([self.env.SCREEN_HEIGHT, 20, self.env.SCREEN_WIDTH, 100, 100], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)


    def reset(self):
        state = self.env.reset()
        return np.array(state, dtype=np.float32)

    def step(self, action, frame_skip=4):
        state, reward, done = self.env.step(action, frame_skip=frame_skip)
        return np.array(state, dtype=np.float32), reward, done, {}

    def render(self, mode='human'):
        self.env.render()

    def close(self):
        self.env.close()
