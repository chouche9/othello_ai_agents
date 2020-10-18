"""
An AI player for Othello.
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

state_dictionary = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    (score1, score2) = get_score(board)
    if color == 1:
        return score1 - score2
    elif color == 2:
        return score2 - score1

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!


############ MINIMAX ######
# #########################
def minimax_min_node(board, color, limit, caching = 0):
    opponent_color = 1
    if color == 1:
        opponent_color = 2
    elif color == 2:
        opponent_color = 1

    if caching:
        if (board, color) in state_dictionary:
            return state_dictionary[(board, color)]

    move_list = get_possible_moves(board, opponent_color)
    if (not move_list) or (limit == 0):
        board_utility = compute_utility(board, color)
        if caching:
            state_dictionary[(board, color)] = (0, 0), board_utility
        return (0, 0), board_utility

    min_move = (0, 0)
    min_value = 1000
    for move in move_list:
        result_board = play_move(board, opponent_color, move[0], move[1])
        next_move, result_board_utility = minimax_max_node(result_board, color, limit - 1)
        if result_board_utility < min_value:
            min_value = result_board_utility
            min_move = move

    if caching:
        state_dictionary[(board, color)] = min_move, min_value

    return min_move, min_value


def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    if caching:
        if (board, color) in state_dictionary:
            return state_dictionary[(board, color)]

    move_list = get_possible_moves(board, color)
    if (not move_list) or (limit == 0):
        board_utility = compute_utility(board, color)
        if caching:
            state_dictionary[(board, color)] = (0, 0), board_utility
        return (0, 0), board_utility

    max_move = (0, 0)
    max_value = -1000
    for move in move_list:
        result_board = play_move(board, color, move[0], move[1])
        next_move, result_board_utility = minimax_min_node(result_board, color, limit - 1)
        if result_board_utility > max_value:
            max_move = move
            max_value = result_board_utility

    if caching:
        state_dictionary[(board, color)] = max_move, max_value

    return max_move, max_value


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    ((i, j), utility) = minimax_max_node(board, color, limit)
    return i, j

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    opponent_color = 1
    if color == 1:
        opponent_color = 2
    elif color == 2:
        opponent_color = 1

    if caching:
        if (board, color) in state_dictionary:
            return state_dictionary[(board, color)]

    move_list = get_possible_moves(board, opponent_color)
    if (not move_list) or (limit == 0):
        board_utility = compute_utility(board, color)
        if caching:
            state_dictionary[(board, color)] = (0, 0), board_utility
        return (0, 0), board_utility

    if ordering:
        board_util_dict = {}
        move_list_ordered = []
        util_list = []
        for move in move_list:
            result_board = play_move(board, opponent_color, move[0], move[1])
            result_util = compute_utility(result_board, color)
            board_util_dict[move] = result_util
            util_list.append(result_util)
        util_list.sort(reverse=True)

        for util in util_list:
            for move in move_list:
                if board_util_dict[move] == util:
                    move_list_ordered.append(move)
        move_list = move_list_ordered

    min_move = (0, 0)
    for move in move_list:
        result_board = play_move(board, opponent_color, move[0], move[1])
        next_move, result_board_alpha = alphabeta_max_node(result_board, color, alpha, beta, limit - 1)
        old_beta = beta
        beta = min(beta, result_board_alpha)
        if beta != old_beta:
            min_move = move
        if beta <= alpha:
            break

    if caching:
        state_dictionary[(board, color)] = min_move, beta
    return min_move, beta


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if caching:
        if (board, color) in state_dictionary:
            return state_dictionary[(board, color)]

    move_list = get_possible_moves(board, color)
    if (not move_list) or (limit == 0):
        board_utility = compute_utility(board, color)
        if caching:
            state_dictionary[(board, color)] = (0, 0), board_utility
        return (0, 0), board_utility

    if ordering:
        board_util_dict = {}
        move_list_ordered = []
        util_list = []
        for move in move_list:
            result_board = play_move(board, color, move[0], move[1])
            result_util = compute_utility(result_board, color)
            board_util_dict[move] = result_util
            util_list.append(result_util)
        util_list.sort(reverse=True)

        for util in util_list:
            for move in move_list:
                if board_util_dict[move] == util:
                    move_list_ordered.append(move)
        move_list = move_list_ordered

    max_move = (0, 0)
    for move in move_list:
        result_board = play_move(board, color, move[0], move[1])
        next_move, result_board_beta = alphabeta_min_node(result_board, color, alpha, beta, limit - 1)
        old_alpha = alpha
        alpha = max(alpha, result_board_beta)
        if alpha != old_alpha:
            max_move = move
        if beta <= alpha:
            break

    if caching:
        state_dictionary[(board, color)] = max_move, alpha

    return max_move, alpha


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    (i, j), utility = alphabeta_max_node(board, color, -100000, 100000, limit)
    return i, j

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
