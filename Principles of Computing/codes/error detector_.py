# sample for error detection work
# http://www.codeskulptor.org/#user41_HkyEsfy7JH_0.py

import random
def generate():
    # generate test cases according to requirements
    length = random.randrange(1, 11)
    board = [0] * length
    for i in range(1, length):
        board[i] = random.randrange(11)
    return board

def sample(board):
    # get the correct result with the test case generated
    import user41_LrDbe6YZgW_0 as sample
    sample_game = sample.SolitaireMancala()
    sample_game.set_board(board)
    return sample_game.plan_moves()

def error(board):
    # get the output from error sample with the test case generated
    import user41_cwKeKZrsxa_1 as error
    error_game = error.SolitaireMancala()
    error_game.set_board(board)
    return error_game.plan_moves()

for i in range(50):
    # run 50 times and find the mismatched cases and
    #output their corresponding test cases
    config = generate()
    sample_move = sample(config)
    error_move = error(config)
    if sample_move != error_move:
        print config
