import numpy as np
import torch
from agent import DQNAgent
from gym_dino_env import DinoGymEnv

# Load environment and agent
env = DinoGymEnv()
state = env.reset()
state_size = len(state)  # Automatically adapts to the state shape
action_size = 2  # [do_nothing, jump]
agent = DQNAgent(state_size, action_size)

# Load trained weights
model_path = "D:/dinobot/ai_dinobot/best_dqn_dino.pth"
agent.q_network.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
agent.q_network.eval()

state = env.reset()
state = np.array(state, dtype=np.float32)
done = False

total_reward = 0
step_count = 0

while not done:
    env.render()
    
    # Choose action using trained policy (no exploration)
    action = agent.act(state, epsilon=0.0)
    
    # Step environment
    next_state, reward, done, _ = env.step(action)
    
    # Track metrics
    total_reward += reward
    step_count += 1

    # Prepare for next step
    next_state = np.array(next_state, dtype=np.float32)
    state = next_state

env.close()

# Print performance metrics
print(f"Total Reward: {total_reward}")
print(f"Episode Length (steps): {step_count}")