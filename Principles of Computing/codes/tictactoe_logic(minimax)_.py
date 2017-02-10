# simpified version
#http://www.codeskulptor.org/#user41_ZqNBVolgQ5VFlPj.py

"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """

    if board.check_win() != None:
        #print 'base case'
        #print 'current player', player
        #print 'current board\n', board
        #print 'the score for best move of oppo:', SCORES[player]*SCORES[board.check_win()]
        #print '\n\n\n'
        return SCORES[board.check_win()], (-1, -1)
    else:
        #print 'recursed'
        empty_squares = board.get_empty_squares()
        max_score = -2
        best_move = (-1,-1)
        for square in empty_squares:
            copy_board = board.clone()
            copy_board.move(square[0], square[1], player)
            new_player = provided.switch_player(player)
            score = mm_move(copy_board, new_player)[0]
            compare_score = score * SCORES[player]
            if compare_score > max_score:
                max_score = compare_score
                best_move = square
                if max_score == 1:
                    return score, best_move
            #print 'current player', player
            #print 'current board\n', board
            #print 'the square to play', square
            #print 'the score for best move of oppo:', score
            #print '\n\n\n'
        return max_score * SCORES[player], best_move

#board = provided.TTTBoard(3)
#board.move(0, 0, provided.PLAYERO)
#board.move(0, 1, provided.PLAYERX)
#board.move(1, 0, provided.PLAYERO)
#board.move(1, 1, provided.PLAYERX)
#board.move(2, 1, provided.PLAYERO)
#board.move(2, 2, provided.PLAYERX)
#board.move(2, 0, provided.PLAYERX)
#print board
#print mm_move(board, provided.PLAYERX)
#print board.get_empty_squares()

#print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

# complex version
#http://www.codeskulptor.org/#user41_pa1Cw0Agb7brr6O.py
"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """

    if board.check_win() != None:
        #print 'base case'
        #print 'current player', player
        #print 'current board\n', board
        #print 'the score for best move of oppo:', SCORES[player]*SCORES[board.check_win()]
        #print '\n\n\n'
        return SCORES[board.check_win()], (-1, -1)
    else:
        #print 'recursed'
        empty_squares = board.get_empty_squares()
        max_score = -2
        min_score = 2
        best_move = (-1,-1)
        for square in empty_squares:
            copy_board = board.clone()
            copy_board.move(square[0], square[1], player)
            new_player = provided.switch_player(player)
            score = mm_move(copy_board, new_player)[0]
            if player == provided.PLAYERX:
                if score > max_score:
                    max_score = score
                    best_move = square
                    if max_score == 1:
                        return max_score, best_move
            else:
                if score < min_score:
                    min_score = score
                    best_move = square
                    if min_score == -1:
                        return min_score, best_move
            #print 'current player', player
            #print 'current board\n', board
            #print 'the square to play', square
            #print 'the score for best move of oppo:', score
            #print '\n\n\n'
        if player == provided.PLAYERX:
            return max_score, best_move
        else:
            return min_score, best_move

#board = provided.TTTBoard(3)
#board.move(0, 0, provided.PLAYERO)
#board.move(0, 1, provided.PLAYERX)
#board.move(1, 0, provided.PLAYERO)
#board.move(1, 1, provided.PLAYERX)
#board.move(2, 1, provided.PLAYERO)
#board.move(2, 2, provided.PLAYERX)
#board.move(2, 0, provided.PLAYERX)
#print board
#print mm_move(board, provided.PLAYERX)
#print board.get_empty_squares()

#print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
