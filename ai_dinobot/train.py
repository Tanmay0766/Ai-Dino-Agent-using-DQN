from gym_dino_env import DinoGymEnv
from agent import DQNAgent
import torch

# Environment setup
env = DinoGymEnv()
state_size = len(env.reset())
action_size = env.action_space.n
agent = DQNAgent(state_size, action_size)

EPISODES = 5000

# Epsilon-greedy parameters
epsilon = 1.0          # Starting epsilon (full exploration)
epsilon_min = 0.05     # Lower min epsilon to keep some exploration
epsilon_decay = 0.995  # Decay rate for epsilon

# For tracking performance
best_reward = -float('inf')

for episode in range(EPISODES):
    state = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        # Choose action (ε-greedy)
        action = agent.act(state, epsilon)
        
        # Take action
        next_state, reward, done, _ = env.step(action, frame_skip=4)        
        # Modify reward to encourage survival
        if done and total_reward < 100:
            reward = -100  # punish crashing too early
        elif not done and reward == 0:
            reward = +1  # reward for surviving 
        
        agent.remember(state, action, reward, next_state, done)
        
        agent.replay()  # Train the Q-network
        
        state = next_state
        total_reward += reward
    
    # Decay epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    # Track best reward
    if total_reward > best_reward:
        best_reward = total_reward
        # Save best model
        torch.save(agent.q_network.state_dict(), "best_dqn_dino.pth")
    
    print(f"Episode {episode + 1}/{EPISODES}, Reward: {total_reward}, Best: {best_reward}, Epsilon: {epsilon:.3f}")

env.close()