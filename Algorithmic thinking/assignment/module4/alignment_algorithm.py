'''
Application of matrices and alignment functions
'''

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    input: a set of characters alphabet and three scores
    output: dictionary of dictionaries whose entries are indexed by 
    pairs of characters in alphabet plus '-'.
    score for any entry indexed by one or more dashes is dash_score
    score for remaining diagonal entries is diag_score
    score for remaining off_diagonal entries is off_diag_score
    '''
    choice_list = list(alphabet)
    choice_list.append('-')
    scoring_dict = {}
    for choice_x in choice_list:
        scoring_dict[choice_x] = {}
    for choice_x in choice_list:
        for choice_y in choice_list:
            if choice_x == '-' or choice_y == '-':
                scoring_dict[choice_x][choice_y] = dash_score
            elif choice_x == choice_y:
                scoring_dict[choice_x][choice_y] = diag_score
            else:
                scoring_dict[choice_x][choice_y] = off_diag_score
    return scoring_dict

#print build_scoring_matrix(["A", "T", "C", "G"], 10, 4, -4)

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    input: two sequences seq_x and seq_y,
    global_flag indicates computing a global alignment matrix or a local one
    output: alignment matrix
    '''
    len_x = len(seq_x)
    len_y = len(seq_y)
    alignment_matrix = [ ["inf" for dummy_col in range(len_y+1)] for dummy_row in range(len_x+1)]
    alignment_matrix[0][0] = 0    
    for index_x in range(1, len_x+1):
        alignment_matrix[index_x][0] = alignment_matrix[index_x-1][0] + \
                                        scoring_matrix[seq_x[index_x-1]]["-"]
        if not global_flag and alignment_matrix[index_x][0] < 0:
            alignment_matrix[index_x][0] = 0
    for index_y in range(1, len_y+1):
        alignment_matrix[0][index_y] = alignment_matrix[0][index_y-1] + \
                                        scoring_matrix["-"][seq_y[index_y-1]]
        if not global_flag and alignment_matrix[0][index_y] < 0:
            alignment_matrix[0][index_y] = 0
    for index_x in range(1, len_x+1):
        for index_y in range(1, len_y+1):
            compare_1 = alignment_matrix[index_x-1][index_y-1] + \
                        scoring_matrix[seq_x[index_x-1]][seq_y[index_y-1]]
            compare_2 = alignment_matrix[index_x-1][index_y] + \
                        scoring_matrix[seq_x[index_x-1]]["-"]
            compare_3 = alignment_matrix[index_x][index_y-1] + \
                        scoring_matrix["-"][seq_y[index_y-1]]
            alignment_matrix[index_x][index_y] = max(compare_1, compare_2, compare_3)
            if not global_flag and alignment_matrix[index_x][index_y] < 0:
                alignment_matrix[index_x][index_y] = 0
    return alignment_matrix

#print compute_alignment_matrix('ACTACT', 'AGCTA', build_scoring_matrix(["A", "T", "C", "G"],2,1,0), True) 

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    input: two sequences, scoring maxtrix and global alignment matrix
    output: a tuple of (score, align_x, align_y) 
    where socre is the score of the global alignment align_x and align_y
    '''    
    index_x = len(seq_x)
    index_y = len(seq_y)
    score = alignment_matrix[index_x][index_y]
    align_x = ''
    align_y = ''
    while index_x != 0 and index_y != 0:
        if alignment_matrix[index_x][index_y] == \
        alignment_matrix[index_x-1][index_y-1] + scoring_matrix[seq_x[index_x-1]][seq_y[index_y-1]]:
            align_x = seq_x[index_x-1] + align_x
            align_y = seq_y[index_y-1] + align_y
            index_x -= 1
            index_y -= 1
        elif alignment_matrix[index_x][index_y] == \
        alignment_matrix[index_x-1][index_y] + scoring_matrix[seq_x[index_x-1]]["-"]:
            align_x = seq_x[index_x-1] + align_x
            align_y = "-" + align_y
            index_x -= 1
        else:
            align_x = "-" + align_x
            align_y = seq_y[index_y-1] + align_y
            index_y -= 1
    while index_x != 0:
        align_x = seq_x[index_x-1] + align_x
        align_y = "-" + align_y
        index_x -= 1
    while index_y != 0:
        align_x = "-" + align_x
        align_y = seq_y[index_y-1] + align_y
        index_y -= 1      
    return (score, align_x, align_y)

#alignment_matrix = compute_alignment_matrix('ACTACT', 'AGCTA', build_scoring_matrix(["A", "T", "C", "G"],2,1,0), True) 
#print compute_global_alignment('ACTACT', 'AGCTA', build_scoring_matrix(["A", "T", "C", "G"],2,1,0), alignment_matrix) 

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    input: two sequences, scoring maxtrix and local alignment matrix
    output: a tuple of (score, align_x, align_y) 
    where socre is the score of the local alignment align_x and align_y
    '''   
    max_score = 0  
    index_x = 0
    index_y = 0
    for index_1 in range(len(seq_x)+1):
        for index_2 in range(len(seq_y)+1):
            score = alignment_matrix[index_1][index_2]
            if score > max_score:
                max_score = score
                index_x = index_1
                index_y = index_2
    align_x = ''
    align_y = ''
    while alignment_matrix[index_x][index_y] != 0:
        if alignment_matrix[index_x][index_y] == \
        alignment_matrix[index_x-1][index_y-1] + scoring_matrix[seq_x[index_x-1]][seq_y[index_y-1]]:
            align_x = seq_x[index_x-1] + align_x
            align_y = seq_y[index_y-1] + align_y
            index_x -= 1
            index_y -= 1
        elif alignment_matrix[index_x][index_y] == \
        alignment_matrix[index_x-1][index_y] + scoring_matrix[seq_x[index_x-1]]["-"]:
            align_x = seq_x[index_x-1] + align_x
            align_y = "-" + align_y
            index_x -= 1
        else:
            align_x = "-" + align_x
            align_y = seq_y[index_y-1] + align_y
            index_y -= 1 
    return (max_score, align_x, align_y)

#alignment_matrix = compute_alignment_matrix('CTA', 'AGCTA', build_scoring_matrix(["A", "T", "C", "G"],2,1,0), False) 
#print compute_local_alignment('CTA', 'AGCTA', build_scoring_matrix(["A", "T", "C", "G"],2,1,0), alignment_matrix) 