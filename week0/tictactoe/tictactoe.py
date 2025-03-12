"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # X goes first, so if there are an equal number of X's and O's, it's X's turn
    # Otherwise, it's O's turn
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # Check each cell on the board
    for i in range(3):
        for j in range(3):
            # If the cell is empty, add it to the possible actions
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action is valid
    if action not in actions(board):
        raise Exception("Invalid action")

    # Make a deep copy of the board to avoid modifying the original
    new_board = copy.deepcopy(board)

    # Get the current player
    current_player = player(board)

    # Make the move
    i, j = action
    new_board[i][j] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there's a winner
    if winner(board) is not None:
        return True

    # Check if the board is full (no empty cells)
    for row in board:
        if EMPTY in row:
            return False

    # Board is full with no winner (tie)
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Get the winner
    game_winner = winner(board)

    # Return utility based on winner
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is terminal, return None
    if terminal(board):
        return None

    current_player = player(board)

    # If it's X's turn, maximize the utility
    if current_player == X:
        best_value = float('-inf')
        best_action = None

        # Try all possible actions
        for action in actions(board):
            # Get the value of the action
            value = min_value(result(board, action))

            # Update best value and action if necessary
            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    # If it's O's turn, minimize the utility
    else:
        best_value = float('inf')
        best_action = None

        # Try all possible actions
        for action in actions(board):
            # Get the value of the action
            value = max_value(result(board, action))

            # Update best value and action if necessary
            if value < best_value:
                best_value = value
                best_action = action

        return best_action


def max_value(board):
    """
    Returns the maximum utility value for a given board.
    """
    # If the board is terminal, return its utility
    if terminal(board):
        return utility(board)

    value = float('-inf')

    # Try all possible actions
    for action in actions(board):
        # Update value with the maximum of the current value and the minimum value of the result
        value = max(value, min_value(result(board, action)))

    return value


def min_value(board):
    """
    Returns the minimum utility value for a given board.
    """
    # If the board is terminal, return its utility
    if terminal(board):
        return utility(board)

    value = float('inf')

    # Try all possible actions
    for action in actions(board):
        # Update value with the minimum of the current value and the maximum value of the result
        value = min(value, max_value(result(board, action)))

    return value