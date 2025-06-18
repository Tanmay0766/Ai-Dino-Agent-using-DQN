import numpy as np
import torch
from agent import DQNAgent
from gym_dino_env import DinoGymEnv
import matplotlib.pyplot as plt

# Configuration
num_episodes = 10
model_path = "D:/dinobot/ai_dinobot/best_dqn_dino.pth"

# Load environment and agent
env = DinoGymEnv()
state = env.reset()
state_size = len(state)
action_size = 2
agent = DQNAgent(state_size, action_size)

# Load trained weights
agent.q_network.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
agent.q_network.eval()

# Metric tracking
episode_rewards = []
episode_lengths = []

for ep in range(num_episodes):
    state = env.reset()
    state = np.array(state, dtype=np.float32)
    done = False
    total_reward = 0
    steps = 0

    while not done:
        env.render()

        action = agent.act(state, epsilon=0.0)
        next_state, reward, done, _ = env.step(action)
        next_state = np.array(next_state, dtype=np.float32)
        state = next_state

        total_reward += reward
        steps += 1

    episode_rewards.append(total_reward)
    episode_lengths.append(steps)
    print(f"Episode {ep+1} -> Reward: {total_reward}, Steps: {steps}")

env.close()

# Print Summary
print("\n===== Performance Summary =====")
print(f"Average Reward:       {np.mean(episode_rewards):.2f}")
print(f"Max Reward:           {np.max(episode_rewards):.2f}")
print(f"Min Reward:           {np.min(episode_rewards):.2f}")
print(f"Average Episode Steps:{np.mean(episode_lengths):.2f}")

# Optional: Plotting
plt.figure(figsize=(10,5))
plt.plot(episode_rewards, marker='o', label='Total Reward')
plt.plot(episode_lengths, marker='x', label='Episode Length')
plt.title("Test Episode Metrics")
plt.xlabel("Episode")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("test_metrics.png")  # Save plot
plt.show()
