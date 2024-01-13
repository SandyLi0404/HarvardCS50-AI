"""
Tic Tac Toe Player
"""

import math
import copy

'''
define possible moves on the board
'''
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


def player(board) -> str:
    """
    Take a board state as input, return which player's turn it is (either X or O).
    In the initial game state, X gets the first move. Subsequently, the player 
    alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input.

    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for square in row:
            if square is not EMPTY:
                count+=1
    if (count == 0 or count % 2 == 0):
        return X
    else:
        return O

def actions(board):
    """
    Each action should be represented as a tuple (i, j) where i corresponds to the row of the 
    move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move.

    Possible moves are any cells on the board that do not already have an X or an O in them.
    Any return value is acceptable if a terminal board is provided as input.

    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    The returned board state should be the board that would result from 
    taking the original input board, and letting the player whose turn it 
    is make their move at the cell indicated by the input action.

    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board=board):
        raise ValueError("invalid move!")
    return_board = copy.deepcopy(board)
    turn = player(board=board)
    if (turn == X):
        return_board[action[0]][action[1]] = X
    else:
        return_board[action[0]][action[1]] = O
    return return_board


def winner(board):
    """
    One can win the game with three of their moves in 
    a row horizontally, vertically, or diagonally.

    Returns the winner of the game, if there is one.
    Returns None if there is no winner in the game.
    """
    for i in range(3):
        if (board[i][0] == board[i][1] and board[i][0] == board[i][2]): # win horizontally
            return board[i][0]
        if (board[0][i] == board[1][i] and board[0][i] == board[2][i]): # win vertically
            return board[0][i]
    # win diagonally
    if (board[0][0] == board[1][1] and board[0][0] == board[2][2]):
        return board[0][0]
    if (board[0][2] == board[1][1] and board[0][2] == board[2][0]):
        return board[0][2]
    else:
        return None


def terminal(board) -> bool:
    """
    If the game is over, either because someone has won the game or because 
    all cells have been filled without anyone winning, the function should return True.
    Otherwise, the function should return False if the game is still in progress.
    Returns True if game is over, False otherwise.
    """
    if (winner(board=board) is not None):
        return True
    elif (len(actions(board=board)) == 0):
        return True
    else:
        return False


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board=board)
    if (win is None):
        return 0
    elif (win == X):
        return 1
    else:
        return -1
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    If the board is a terminal board, return None.
    """
    if (terminal(board=board)):
        return None
    else:
        if (player(board=board) == X):
            move = max_value(board=board)
            return move[1]

        else:
            move = min_value(board=board)
            return move[1]

def max_value(board):
    if (terminal(board=board)):
        return [utility(board=board), None]
    value = -2
    act = None
    for action in actions(board=board):
        new_value = min_value(board=result(board=board, action=action))[0]
        value = max(value, new_value)
        if (value == new_value):
            act = action
    return [value, act]

def min_value(board):
    if (terminal(board=board)):
        return [utility(board=board), None]
    value = 2
    act = None
    for action in actions(board=board):
        new_value = max_value(board=result(board=board, action=action))[0]
        value = min(value, new_value)
        if (value == new_value):
            act = action
    return [value, act]