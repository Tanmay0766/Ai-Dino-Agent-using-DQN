# 🦖 Chrome Dino Reinforcement Learning Agent

This project showcases a Deep Q-Network (DQN) based reinforcement learning agent trained to play the Chrome Dino game. Built using PyGame and Gym style wrapper, the agent learns to survive and jump over obstacles effectively, mimicking human play through observation-based state input.

## Demo Link: 
https://www.linkedin.com/posts/tanmay-singh-429ab81b9_ai-reinforcementlearning-python-activity-7341131692671234049-KaB8?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAADLi-2EBDMofotInT29A0nDfI1120hvUmCE

## 🎮 Features

- **Custom Game Environment**: Recreated Chrome Dino game using PyGame
- **Gym-Compatible**: Environment is wrapped using Gym style wrapper for easy training/testing
- **DQN Agent**: Deep Q-Learning with experience replay and target network
- **Frame Skipping**: Improves training efficiency and simulates human-like reaction
- **Metrics & Logging**: Training reward graphs and test performance included

## 🚀 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/Tanmay0766/Ai-Dino-Agent-using-DQN.git
   cd Ai-Dino-Agent-using-DQN
   
2. Create the Conda Environment:
   
   Create a new environment using the provided environment.yml file:
   ```bash
   conda env create -f environment.yml
   ```
   Activate the Environment:```
   conda activate your-env-name```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Run training:
   ```bash
   python train.py
   
8. Test the trained agent:
   ```bash
   python test.py
   
## 🧠 State Description
The agent receives the following state vector:

1. Dino's vertical position
2. Vertical velocity
3. Distance to next cactus
4. Cactus height
5. Cactus width

## 📂 File Structure
1. game.py_# Original dino game
2. dino_env.py_# Pygame environment logic
3. gym_dino_env.py_# Gym wrapper
4. agent.py_# DQN agent
5. train.py_# Training script
6. test1.py_# Testing script
7. test2.py_# Test metrices and graph
8. best_dqn_dino.pth_# Saved model (trained)
9. README.md

## 📜 License
This project is licensed under the **MIT License.**
