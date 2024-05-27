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
    if terminal(board):
        return None

    emptySpaces = sum([i.count(EMPTY) for i in board])
    if emptySpaces % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return None
    
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions
            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    
    (i, j) = action

    if 0 <= i < 3 and 0 <= j < 3:
        newBoard = copy.deepcopy(board)
        if newBoard[i][j] != EMPTY:
            raise Exception
        newBoard[i][j] = player(newBoard)
        return newBoard
    else:
        raise Exception
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if all(x == row[0] for x in row) and row[0] != EMPTY:
            return row[0]
    for col in range(3):
        if all(board[i][col] == board[0][col] for i in range(3)) and board[0][col] != EMPTY:
            return board[0][col]

    if all(board[i][i] == board[0][0] for i in range(3)) and board[0][0] != EMPTY:
        return board[0][0]
    if all(board[i][2 - i] == board[0][2] for i in range(3)) and board[0][2] != EMPTY:
        return board[0][2]

    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    newBoard = copy.deepcopy(board)
    if terminal(newBoard):
        return None

    bot = player(newBoard)
    if bot == X:
        m = maximizer(newBoard)
        return m[1]
    else:
        m = minimizer(newBoard)
        return m[1]
        

def maximizer(board):
    v = -math.inf
    optimalMove = None
    if terminal(board):
        return (utility(board), optimalMove)
    for action in actions(board):
        m = minimizer(result(board, action))[0]
        if v < m:
            v = m
            optimalMove = action
    
    return (v, optimalMove)

def minimizer(board):
    v = math.inf
    optimalMove = None
    if terminal(board):
        return (utility(board), optimalMove)
    for action in actions(board):
        m = maximizer(result(board, action))[0]
        if v > m:
            v = m
            optimalMove = action
    return (v, optimalMove)