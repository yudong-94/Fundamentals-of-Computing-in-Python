# Stopwatch: The Game
# http://www.codeskulptor.org/#user40_0V3lnOAjoDOwT27.py

# define global variables
import simplegui

t = 0
wins = 0
tries = 0
running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global str_time
    if t // 600 == 0:
        minutes = 0
    else:
        minutes = t//600
    seconds = (t - 600* minutes) // 10
    tenth_seconds =  t - 600 * minutes - 10* seconds
    if seconds < 10:
        str_time = str(minutes)+":0"+str(seconds)+"."+str(tenth_seconds)
    else:
        str_time = str(minutes)+":"+str(seconds)+"."+str(tenth_seconds)
    return str_time

def scores():
    global wins, tries
    if running == False:
        wins = wins
        tries = tries
    elif t % 10 == 0:
        wins = wins + 1
        tries = tries + 1
    else:
        tries = tries + 1

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    frame.set_draw_handler(draw)

def stop():
    global running
    running = timer.is_running()
    timer.stop()
    scores()
    frame.set_draw_handler(draw)

def reset():
    timer.stop()
    global t, wins, tries
    t = 0
    wins = 0
    tries = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global t
    t = t + 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(t),[100,120], 48, "White")
    canvas.draw_text(str(wins)+"/"+str(tries), [250,20], 24, "White")

# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start, 100)
frame.add_label("")
frame.add_button("Stop", stop, 100)
frame.add_label("")
frame.add_button("Reset", reset, 100)

# start frame
frame.start()
frame.set_draw_handler(draw)

# Please remember to review the grading rubric
