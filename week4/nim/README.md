# Nim Game AI

## What is Nim?
Nim is a simple game where:
- We start with piles of objects
- Players take turns removing objects from piles
- On your turn, you can take any number of objects from one pile
- The player who takes the last object loses

## About This Project
This project creates an AI that learns to play Nim by itself. The AI uses reinforcement learning, which means it learns by playing many games and remembering what works well.

## How Solution Works

### 1. Q-Learning
The AI uses a method called Q-learning. This means:
- It keeps track of how good each move is in each game state
- It saves these values in a Q-table (just a dictionary)
- Better moves get higher Q-values
- Worse moves get lower Q-values

### 2. Key Functions Implemented

#### get_q_value
This function finds how good a move is:
- It checks if we already know the value of this move
- If we do, it returns that value
- If we don't, it returns 0

#### update_q_value
This function updates our knowledge after making a move:
- It uses the reward we got
- It uses what we expect to happen next
- It slowly adjusts our knowledge using the learning rate (alpha)

#### best_future_reward
This function finds the best possible next move:
- It looks at all possible moves
- It returns the value of the best one
- If there are no moves, it returns 0

#### choose_action
This function decides what move to make:
- Sometimes it tries random moves to explore (when epsilon is true)
- Most of the time it picks the best move it knows
- If multiple moves seem equal, it picks one randomly

## How to Run the Game
1. Run `python play.py`
2. The AI will train by playing 10,000 games against itself
3. After training, you can play against the AI
4. Follow the prompts to choose a pile and how many objects to take

## How the AI Learns
- When the AI wins, it gets a reward of +1
- When the AI loses, it gets a penalty of -1
- The AI remembers which moves led to wins
- After many games, it learns the best strategy
- It uses "exploration" to try new moves sometimes
- It uses "exploitation" to use its best known moves most of the time

## Why This Works
After training, the AI learns patterns about what makes a good move in Nim. It doesn't know the mathematical theory, but it figures out through practice what works!

## Understanding States and Actions
- A "state" is just the current size of all piles (like [1, 3, 5, 7])
- An "action" is taking some objects from a pile (like "take 2 objects from pile 1")
- The Q-table connects states and actions to values
- The AI learns which actions are good in which states

## The Learning Formula
The AI updates its knowledge using a simple formula:
- It starts with what it already knows
- It looks at the reward it got
- It considers what might happen next
- It updates its knowledge a little bit at a time

## Balancing Exploration and Exploitation
- "Exploration" means trying new moves to discover better strategies
- "Exploitation" means using the best moves we already know
- The "epsilon" value controls how often the AI explores
- With a small epsilon, the AI mostly uses what it knows but sometimes tries something new

## The Training Process
During training:
1. The AI plays against itself
2. It makes moves based on what it knows and some randomness
3. It updates its knowledge after each move
4. Over time, it learns which moves lead to winning
5. After thousands of games, it becomes very good at Nim