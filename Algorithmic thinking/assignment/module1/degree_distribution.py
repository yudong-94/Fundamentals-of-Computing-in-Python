# http://www.codeskulptor.org/#user41_XKvs1N17o30ix9c.py

'''
graph presentation
'''

EX_GRAPH0 = {0: set([1, 2]),
            1: set([]),
            2: set([])}
EX_GRAPH1 = {0: set([1, 4, 5]),
            1: set([2, 6]),
            2: set([3]),
            3: set([0]),
            4: set([1]),
            5: set([2]),
            6: set([])}
EX_GRAPH2 = {0: set([1, 4, 5]),
            1: set([2, 6]),
            2: set([3, 7]),
            3: set([7]),
            4: set([1]),
            5: set([2]),
            6: set([]),
            7: set([3]),
            8: set([1, 2]),
            9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    '''
    for the given num_nodes,
    return a complete directed graph in dictionary
    with all possible edges except self-loop.
    '''
    graph = {}
    complete_set = set([dummy_i for dummy_i in range(num_nodes)])
    if num_nodes > 0:
        for dummy_i in range(num_nodes):
            graph[dummy_i] = complete_set.difference(set([dummy_i]))
    return graph

# print make_complete_graph(3)

def compute_in_degrees(digraph):
    '''
    for a given directed graph,
    compute in_degrees for each nodes,
    and return as a dictionary.
    '''
    degrees = {}
    for node in digraph:
        counter = 0
        for node_2 in digraph:
            if node in digraph[node_2]:
                counter += 1
        degrees[node] = counter
    return degrees

# print compute_in_degrees(make_complete_graph(3))
# print compute_in_degrees(EX_GRAPH1)

def in_degree_distribution(digraph):
    '''
    for a given directed graph,
    compute number of nodes for each valid in-degree value.
    '''
    distribution = {}
    degrees = compute_in_degrees(digraph)
    in_degrees = degrees.values()
    for degree in in_degrees:
        counter = 0
        for node in degrees:
            if degrees[node] == degree:
                counter += 1
        distribution[degree] = counter
    return distribution

# print in_degree_distribution(make_complete_graph(3))
# print in_degree_distribution(EX_GRAPH1)
