# Rock-paper-scissors-lizard-Spock
# http://www.codeskulptor.org/iipp-practice-experimental/#user40_Wh1T1oOg9Gdwv5U.py

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    # delete the following pass statement and fill in your code below
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "Error: Invalid name."


    # convert name to number using if/elif/else


def number_to_name(number):
    # delete the following pass statement and fill in your code below
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "Error: Invalid number."


    # convert number to a name using if/elif/else


def rpsls(player_choice):
    # delete the following pass statement and fill in your code below
    print " "
    print "Player chooses " + str(player_choice)
    player_number = name_to_number(player_choice)

    import random
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses " + str(comp_choice)

    comparison = (comp_number - player_number) % 5
    if comparison ==1 or comparison ==2:
        print "Computer wins!"
    elif comparison == 0:
        print "Player and computer tie!"
    else:
        print "Player wins!"

def enter(choice):
    rpsls(choice)

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

import simplegui

frame = simplegui.create_frame ("Rplsls", 200, 200)
frame.add_input("Enter your choice", enter ,100)
