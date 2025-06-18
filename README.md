# 🦖 Chrome Dino Reinforcement Learning Agent

This project showcases a Deep Q-Network (DQN) based reinforcement learning agent trained to play the Chrome Dino game. Built using PyGame and OpenAI Gym, the agent learns to survive and jump over obstacles effectively, mimicking human play through observation-based state input.

## 🎮 Features

- **Custom Game Environment**: Recreated Chrome Dino game using PyGame
- **Gym-Compatible**: Environment is wrapped using OpenAI Gym for easy training/testing
- **DQN Agent**: Deep Q-Learning with experience replay and target network
- **Frame Skipping**: Improves training efficiency and simulates human-like reaction
- **Metrics & Logging**: Training reward graphs and test performance included

## 🚀 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/Tanmay0766/Ai-Dino-Agent-using-DQN.git
   cd Ai-Dino-Agent-using-DQN

2. Install dependencies:
   _pip install -r requirements.txt_

3. Run training:
   _python train.py_
   
4. Test the trained agent:
   _python test.py_
   
## 🧠 State Description
The agent receives the following state vector:

1. Dino's vertical position
2. Vertical velocity
3. Distance to next cactus
4. Cactus height
5. Cactus width

## 📂 File Structure
.
|-- dino_env.py           # Pygame environment logic
|-- gym_dino_env.py       # Gym wrapper
|-- agent.py              # DQN agent
|-- train.py              # Training script
|-- test1.py              # Testing script
|-- test2.py              # Test metrices and graph
|-- best_dqn_dino.pth     # Saved model (trained)
└-- README.md

## 📜 License
This project is licensed under the **MIT License.**
