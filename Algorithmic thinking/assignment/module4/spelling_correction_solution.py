import application4_provided as load
import alignment_algorithm as algorithm

##############Q8
word_list = load.read_words("assets_scrabble_words3.txt")

def check_spelling(checked_word, dist, word_list):
    checked_len = len(checked_word)
    scoring_matrix = algorithm.build_scoring_matrix("abcdefghijklmnopqrstuvwxyz",2,1,0)
    close_word = []
    for word in word_list:
        alignment_matrix = algorithm.compute_alignment_matrix(checked_word, word,
                                                              scoring_matrix, True)
        alignment = algorithm.compute_global_alignment(checked_word, word, 
                                                       scoring_matrix, alignment_matrix)
        if checked_len + len(word) - alignment[0] <= dist:
            close_word.append(word)
    return set(close_word)

close_humble = check_spelling("humble", 1, word_list)
print close_humble
close_firefly = check_spelling("firefly", 2, word_list)
print close_firefly

## set(['bumble', 'humbled', 'tumble', 'humble', 'rumble', 'humbler', 'humbles', 'fumble', 'humbly', 'jumble', 'mumble'])
## set(['firefly', 'tiredly', 'freely', 'fireclay', 'direly', 'finely', 'firstly', 'liefly', 'fixedly', 'refly', 'firmly'])
