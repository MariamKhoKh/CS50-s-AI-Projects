# Tic-Tac-Toe AI

This project implements an artificial intelligence that plays Tic-Tac-Toe optimally using the Minimax algorithm. The AI can never lose - it will either win (if the human player makes a mistake) or force a tie.

## Problem Statement

The full problem statement can be found at: https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/

## Solution Description

The solution uses the Minimax algorithm, which is a decision-making algorithm used in game theory. Here's how it works:

### Key Components

1. **Player Function**: Determines whose turn it is (X or O) by counting the number of X's and O's on the board.

2. **Actions Function**: Finds all empty cells on the board where a player can place their mark.

3. **Result Function**: Creates a new board with the result of a move without changing the original board.

4. **Winner Function**: Checks if anyone has won by looking at rows, columns, and diagonals.

5. **Terminal Function**: Determines if the game is over (someone won or the board is full).

6. **Utility Function**: Assigns a value to the final game state:
   - 1 if X wins
   - -1 if O wins
   - 0 for a tie

7. **Minimax Function**: The main algorithm that:
   - For X (maximizing player): Chooses the move that leads to the highest value
   - For O (minimizing player): Chooses the move that leads to the lowest value

### How Minimax Works

It is thinking ahead like a chess player:
- considers all possible moves it could make
- then it considers all possible responses by the opponent
- then all possible responses to those responses, and so on until reaching the end of the game
- assigns a value to each final position (win, lose, or tie)
- works backward, assuming that:
  - the AI will always choose the best move for itself
  - the opponent will always choose the best move for themselves

This way, the AI can choose the optimal move in any situation, guaranteeing it will never lose.

## How to Run
1. Install the required packages using `pip3 install -r requirements.txt`
2. Run the game using `python runner.py`

## Usage

When you run the game:
1. choose whether to play as X or O
2. the game board will appear
3. take turns with the AI by clicking on empty cells
4. the game will end when someone wins or the board is full (tie)
5. click "Play Again" to start a new game
