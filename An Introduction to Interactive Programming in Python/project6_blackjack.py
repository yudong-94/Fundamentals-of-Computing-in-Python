# Blackjack
# http://www.codeskulptor.org/#user40_b06kFMCAFJiUp04.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = "Hit or Stand?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.card = []

    def __str__(self):
        s = ""
        for i in range(len(self.card)):
            s+= " "
            s+= str(self.card[i])
        return "Hand contains"+ s

    def add_card(self, card):
        self.card.append(card)

    def get_value(self):
        hand_value = 0
        Ace = False
        for card in self.card:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                Ace = True
        if Ace and hand_value + 10 <= 21:
            return hand_value + 10
        else:
            return hand_value

    def draw(self, canvas, pos):
        i = 0
        for card in self.card:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.get_rank()),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.get_suit()))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, (pos[0] + 100 * i, pos[1]), CARD_SIZE)
            i += 1

# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        n = 0
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))


    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        s = ""
        for card in self.deck:
            s += " "
            s += str(card)
        return "Deck contains" + s

#define event handlers for buttons
def deal():
    global new, outcome, dealer_hand, player_hand, in_play, canvas, score
    if in_play:
        outcome = "Last game interrupted. Hit or stand?"
        score -= 1
        print "score is now " + str(score)
    else:
        outcome = "Hit or Stand?"
    new = Deck()
    new.shuffle()
    print new
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(new.deal_card())
    dealer_hand.add_card(new.deal_card())
    player_hand.add_card(new.deal_card())
    dealer_hand.add_card(new.deal_card())
    print player_hand
    print dealer_hand
    print outcome
    in_play = True

def hit():
    global in_play, score, hint, outcome
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(new.deal_card())
        print player_hand

    # test whether player busted
        if player_hand.get_value() > 21:
            outcome = "Player Busted. New deal?"
            in_play = False
            score -= 1
            print outcome
            print "score is now "+ str(score)

def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global dealer_hand, player_hand, outcome, in_play, score
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(new.deal_card())
        print dealer_hand
        if dealer_hand.get_value() > 21:
            outcome = "Dealer Busted."
            score += 1
            print "score is now "+ str(score)
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer wins."
                score -= 1
                print "score is now "+ str(score)
            else:
                outcome = "Player wins."
                score += 1
                print "score is now "+ str(score)
        outcome += " New Deal?"
        in_play = False
        print outcome


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", (200, 50), 36, "Black")
    canvas.draw_text(outcome, (50, 125), 24, "Red")
    canvas.draw_text("Score: " + str(score), (450, 125), 24, "Red")
    canvas.draw_text("Dealer's hand", (50, 200), 24, "Black")
    canvas.draw_text("Player's hand", (50, 370), 24, "Black")
    dealer_hand.draw(canvas, [90, 260])
    player_hand.draw(canvas, [90, 430])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (90, 260), CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
