# Guess the number
# http://www.codeskulptor.org/#user40_U0bP6UNbKDnO4G3.py

# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui
import math

uplimit = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(0,uplimit)
    global count
    count = int(math.ceil(math.log(uplimit, 2)))
    print "New game. Range is from 0 to "+str(uplimit)+"."
    print "You have "+str(count)+" chances to guess."
    print " "


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global uplimit
    uplimit = 100
    new_game()


def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global uplimit
    uplimit = 1000
    new_game()

def input_guess(guess):
    # main game logic goes here
    guess_number = int(guess)
    global count
    count = count - 1
    print "Guess was "+ guess
    if count == 0 and guess_number <> secret_number:
        print "Wrong guess! You have run out of guesses!"
        print "The secret number is "+str(secret_number)+"."
        print " "
        print "Cheer up! Let's play again: "
        new_game()
        print " "
    elif guess_number > secret_number:
        print "Number of remaining guesses is ", count
        print "Lower!"
        print " "
    elif guess_number < secret_number:
        print "Number of remaining guesses is ", count
        print "Higher!"
        print " "
    else:
        print "Correct!"
        print " "
        print "Congradulations! Let's play once more: "
        new_game()
        print" "



# create frame
frame= simplegui.create_frame("Guess the number", 200, 300)
frame.add_button("Range is [0,100)", range100, 150)
frame.add_button("Range is [0,1000)", range1000, 150)
frame.add_input("Enter a guess: ", input_guess, 100)

# register event handlers for control elements and start frame
frame.start()

# call new_game
new_game()
