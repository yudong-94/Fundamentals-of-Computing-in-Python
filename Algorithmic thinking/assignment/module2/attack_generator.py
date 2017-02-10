# general imports
import random

# helper function

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

#################testing cases#############
GRAPH0 = {0: set([3, 5]),
          1: set([4, 6, 8]),
          2: set([3, 5, 7]),
          3: set([0, 2, 4, 6, 7, 8]),
          4: set([1, 3, 5, 7]),
          5: set([0, 2, 4, 6, 8]),
          6: set([1, 3, 5, 7]),
          7: set([2, 3, 4, 6, 8]),
          8: set([1, 3, 5, 7])}

##########################################################
# functions to simulate the attack

def random_order(graph):
    '''
    return a list of all the nodes in the graph in random order
    '''
    nodes = graph.keys()
    random.shuffle(nodes)
    return nodes

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def fast_targeted_order(ugraph):
    '''
    fast implementation of target_order function
    retun an ordered list of nodes in decreasing order of their degrees
    '''
    degree_sets = {}
    copy_ugraph = copy_graph(ugraph)
    for degree in range(len(copy_ugraph)):
        degree_sets[degree] = set([])
    for node in copy_graph(ugraph).keys():
        current_degree = len(copy_ugraph[node])
        degree_sets[current_degree].add(node)
    order = []
    for degree in range(len(copy_ugraph)-1, -1, -1):
        while len(degree_sets[degree]) != 0:
            random_node = random.choice(list(degree_sets[degree]))
            degree_sets[degree].remove(random_node)
            for neighbor in copy_ugraph[random_node]:
                neighbor_degree = len(copy_ugraph[neighbor])
                degree_sets[neighbor_degree].remove(neighbor)
                degree_sets[neighbor_degree - 1].add(neighbor)
            order.append(random_node)
            delete_node(copy_ugraph, random_node)
    return order

# print targeted_order(GRAPH0)
# print fast_targeted_order(GRAPH0)