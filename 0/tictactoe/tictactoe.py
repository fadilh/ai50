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
    newBoard = copy.deepcopy(board)

    newBoard[i][j] == player(newBoard)
    
    return newBoard
    

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
    
    return not any(any(i == EMPTY for i in row) for row in board)


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
    if terminal(board):
        return None

    possibleMoves = actions(board)
    scores = []
    for action in possibleMoves:
        bot = player(board)
        if bot == X:
            score = maximizer(result(board, action))
        else:
            score = minimizer(result(board, action))
        
        scores.append(score)


    if len(scores) == 1:
        return scores[0]

    optimalMove = possibleMoves[0]
    optimalValue = scores[0]

    for i in range(len(possibleMoves)):
        if player(board) == X:
            if optimalValue < scores[i]:
                optimalMove = possibleMoves[i]
                optimalValue = scores[i]
                if optimalValue == 1:
                    return optimalMove
        else:
            if optimalValue > scores[i]:
                optimalMove = possibleMoves[i]
                optimalValue = scores[i]
                if optimalValue == -1:
                    return optimalMove

    return optimalMove

def maximizer(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, minimizer(result(board, action)))
    return v

def minimizer(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, maximizer(result(board, action)))
    return v