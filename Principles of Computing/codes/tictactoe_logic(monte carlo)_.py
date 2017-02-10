# http://www.codeskulptor.org/#user41_A9yVpwrc7NGxFDu.py

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50         # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

def mc_trial(board, player):
    '''
    play a game starting with the given player
    by making random moves, alternating between players,
    until game ends.
    '''
    state = board.check_win()
    while state == None:
        empty_squares = board.get_empty_squares()
        choice = random.choice(empty_squares)
        board.move(choice[0], choice[1], player)
        state = board.check_win()
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    '''
    take a completed game's board,
    and update the scores cumulatively
    throughout all trails for one move.
    '''
    length = board.get_dim()
    winner = board.check_win()
    status_to_score = {provided.DRAW:0, player:1, provided.switch_player(player):-1}
    for row in range(length):
        for column in range(length):
            status = board.square(row, column)
            if status == player:
                scores[row][column] += SCORE_CURRENT * status_to_score[winner]
            elif status == provided.switch_player(player):
                scores[row][column] -= SCORE_OTHER * status_to_score[winner]

def get_best_move(board, scores):
    '''
    take the score board for all of the trials for one move,
    and return the one empty square with
    highest cumulative score.
    '''
    empty_squares = board.get_empty_squares()
    #print 'empty squares'
    #print empty_squares
    if empty_squares == []:
        return None
    highest_score = scores[empty_squares[0][0]][empty_squares[0][1]]
    best_move = []
    for square in empty_squares:
        score = scores[square[0]][square[1]]
        if score > highest_score:
            best_move = [square]
            highest_score = score
        elif score == highest_score:
            best_move.append(square)
        #print square
        #print best_move
    #print best_move
    move_selected = random.choice(best_move)
    return move_selected

def mc_move(board, player, trials):
    '''
    given current board,
    make trial moves using mc_trial(),
    calculate score board using mc_update_scores(),
    and find the best move using get_best_move().
    '''
    length = board.get_dim()
    scores_board = [[0 for dummy_col in range(length)] for dummy_row in range(length)]
    current_board = board.clone()
    for dummy_trail in range(trials):
        #print player
        mc_trial(current_board, player)
        #print 'board\n'
        #print current_board
        #print player
        mc_update_scores(scores_board, current_board, player)
        #print 'scores\n'
        #print scores_board
        current_board = board.clone()
    return get_best_move(current_board, scores_board)



# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
