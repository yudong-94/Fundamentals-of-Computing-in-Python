"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# http://www.codeskulptor.org/#user41_83LnQWWKg06l4fJ.py
# game link: https://cardgames.io/yahtzee/

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

#print gen_all_sequences([1, 2], 2)

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    max_score = 0
    for dice_num in range(1,max(hand) + 1):
        current_score = 0
        for hand_num in hand:
            if dice_num == hand_num:
                current_score += dice_num
        if current_score > max_score:
            max_score = current_score
    return max_score

#print score((3, 8, 7, 3, 7, 3, 3))

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of scores based on held_dice
    given that there are num_free_dice to be rolled,
    each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    all_outcomes = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    total_scores = 0
    for outcome in all_outcomes:
        #print "outcome", outcome
        total_scores += score(outcome + held_dice)
        #print 'score of', str(outcome + held_dice), score(outcome + held_dice)
        #print "total score", total_scores
    return float(total_scores)/len(all_outcomes)

print expected_value((3,3), 8, 5)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_subsets = set([()])
    choice_matrix = gen_all_sequences([0, 1], len(hand))
    for matrix in choice_matrix:
        temp_tuple = ()
        for idx in range(len(hand)):
            if matrix[idx] == 1:
                temp_lst = []
                temp_lst.append(hand[idx])
                temp_tuple += tuple(temp_lst)
        all_subsets.add(temp_tuple)
    return all_subsets

#print gen_all_holds((1,2,2))


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_score = 0
    max_hold = ()
    for hold in all_holds:
        expected_score = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if expected_score > max_score:
            max_score = expected_score
            max_hold = hold

    return (max_score, max_hold)

#print strategy((1, 3, 3), 3)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


#run_example()
#print gen_all_sequences([1, 2, 3], 2)


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
