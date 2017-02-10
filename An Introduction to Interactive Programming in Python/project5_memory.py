# implementation of card game - Memory
# http://www.codeskulptor.org/#user40_VO6nyyj4uA6jl5D.py

import simplegui
import random

exposed = [False] * 16
turns = 0

# helper function to initialize globals
def new_game():
    global list1, list2, card_list, exposed, turns, state, win
    list1 = range(8)
    list2 = range(8)
    card_list = list1 + list2
    random.shuffle(card_list)
    exposed = [False] * 16
    turns = 0
    label.set_text("Turns = " + str(turns))
    state = 0
    win = False

# define event handlers
def mouseclick(pos):
    global state, exposed, turns, pair1, pair2, win
    for card in range(16):
        if card * 50 <= pos[0] < 50 + card * 50 and exposed[card] == False:
            if state == 0:
                turns += 1
                state = 1
                exposed[card] = True
                pair1 = card
            elif  state == 2:
                turns += 1
                state = 1
                if card_list[pair1] <> card_list[pair2]:
                    exposed[pair1] = False
                    exposed[pair2] = False
                exposed[card] = True
                pair1 = card
            elif state == 1:
                state = 2
                exposed[card] = True
                pair2 = card
    label.set_text("Turns = " + str(turns))
    if exposed == [True] * 16:
        win = True

# cards are logically 50x100 pixels in size
def draw(canvas):
    if win == True:
        canvas.draw_text("You win in " + str(turns) + " turns!", [200, 60], 50, "Red")
    else:
        for i in range(16):
            canvas.draw_text(str(card_list[i]), [20 + 50 * i ,55],
                            25, "White")
        for j in range(16):
            if exposed[j] == False:
                canvas.draw_polygon([(50 * j, 0), (50 + 50 * j, 0),
                                    (50 + 50 * j, 100), (50 * j, 100)],
                                    5, "White", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
