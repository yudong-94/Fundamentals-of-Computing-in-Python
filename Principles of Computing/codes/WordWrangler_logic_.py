"""
Student code for Word Wrangler game
"""

# http://www.codeskulptor.org/#user41_Ou3kq5kriOJqCSm.py

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"
codeskulptor.set_timeout(30)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    index = 0
    copy_list = list(list1)
    while index < len(copy_list):
        other_list = list(copy_list)
        other_list.remove(copy_list[index])
        if copy_list[index] in other_list:
            copy_list.pop(index)
        else:
            index += 1

    return copy_list

#print remove_duplicates([1, 2, 2, 3, 4, 4, 4])

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersection_list = []
    copy_list1 = list(list1)
    copy_list2 = list(list2)
    while len(copy_list1)>0 and len(copy_list2)>0:
        if copy_list1[0] == copy_list2[0]:
            intersection_list.append(copy_list2[0])
            copy_list1.pop(0)
            copy_list2.pop(0)
            #print intersection_list
        elif copy_list1[0] < copy_list2[0]:
            copy_list1.pop(0)
        else:
            copy_list2.pop(0)

    return intersection_list

#print intersect([1, 2, 5], [2, 3, 4, 5])

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    copy_list1 = list(list1)
    copy_list2 = list(list2)
    merge_list = []
    while len(copy_list1)>0 and len(copy_list2)>0:
        if copy_list1[0] < copy_list2[0]:
            merge_list.append(copy_list1[0])
            copy_list1.pop(0)
        else:
            merge_list.append(copy_list2[0])
            copy_list2.pop(0)
    if len(copy_list1)>0:
        merge_list += copy_list1
    elif len(copy_list2)>0:
        merge_list += copy_list2
    return merge_list

#print merge([1, 2, 4], [0, 2, 3, 5])

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 0:
        return []
    if len(list1) == 1:
        return list1
    else:
        length = len(list1)
        half = length / 2
        half1_sorted = merge_sort(list1[:half])
        half2_sorted = merge_sort(list1[half:])
        #print half1_sorted, half2_sorted
        return merge(half1_sorted, half2_sorted)

#print merge_sort([6, 2, 3, 7, 1, 5, 4, 8])

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    if len(word) == 1:
        return ['', word]
    else:
        first = word[0]
        #print 'first', str(first)
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        #print 'rest strings', str(rest_strings)
        new_strings = []
        for string in rest_strings:
            #print 'string', str(string)
            for index in range(len(string)):
                new_strings.append(string[:index]+first+string[index:])
            new_strings.append(string+first)
        new_strings +=rest_strings
        return new_strings

#print gen_all_strings('aab')

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    dictionary = netfile.read()
    return dictionary.split('\n')

#print load_words(WORDFILE)

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
