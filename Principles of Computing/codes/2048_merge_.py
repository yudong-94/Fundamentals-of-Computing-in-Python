"""
Merge function for 2048 game.
"""
# http://www.codeskulptor.org/#user41_bUxmjqoLFAg46WM.py

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    valid_entry = []
    for entry in line:
        if entry != 0:
            valid_entry.append(entry)
    for index in range(len(valid_entry) - 1):
        # if next number is the same as the current number:
        # double current number and delete the next number from the list.
        # therefore the next loop will check the pair after current pair.
        # for each loop, check how much number left in the list:
        # if one or less(length-index <= 2): end the loop (no more pairs).
        if valid_entry[index] == valid_entry[index + 1]:
            valid_entry[index] *= 2
            valid_entry.pop(index + 1)
        if len(valid_entry) - index <= 2:
            break
    zero_num = len(line) - len(valid_entry)
    return valid_entry + [0] * zero_num

print merge([2, 0, 2, 4])
print merge([0, 0, 2, 2])
print merge([2, 2, 0, 0])
print merge([2, 2, 2, 2, 2])
print merge([8, 16, 16, 8])
