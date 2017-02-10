'''
BFS-Visited
'''

#################testing cases#############
GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}

GRAPH1 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}

GRAPH2 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([2, 4, 6, 8]),
          4: set([1, 3, 5, 7]),
          5: set([2, 4, 6, 8]),
          6: set([1, 3, 5, 7]),
          7: set([2, 4, 6, 8]),
          8: set([1, 3, 5, 7])}

##########################################

from collections import deque
import random

def bfs_visited(ugraph, start_node):
    '''
    ugraph is the undirected graph.
    this function returns the set consisting of all nodes
    that are visited by a breadth-first search 
    tht starts at start_node.
    '''
    bfs_queue = deque()
    visited = [start_node]
    bfs_queue.append(start_node)
    while len(bfs_queue) != 0:
        current_node = bfs_queue.popleft()
        for neighbor_node in ugraph[current_node]:
            if neighbor_node not in visited:
                visited.append(neighbor_node)
                bfs_queue.append(neighbor_node)
    return set(visited)

def cc_visited(ugraph):
    '''
    return a list of sets
    where each set consists of all the nodes (and nothing else) 
    in a connected component.
    '''
    remaining_nodes = set(ugraph.keys())
    connected_components = []
    while len(remaining_nodes) != 0:
        random_node = random.choice(list(remaining_nodes))
        visited = bfs_visited(ugraph, random_node)
        connected_components.append(visited)
        remaining_nodes = remaining_nodes.difference(visited)
    return connected_components

def largest_cc_size(ugraph):
    '''
    returns the size of the largest connected component in ugraph
    '''
    connected_components = cc_visited(ugraph)
    largest_size = 0
    for connected_sets in connected_components:
        if len(connected_sets) > largest_size:
            largest_size = len(connected_sets)
    return largest_size

def compute_resilience(ugraph, attack_order):
    '''
    attak_order is a list of nodes to attack on.
    for each node attacked, the function removes the given nodes and its edges
    and computes the size of the largest connected component.
    the first entry of the returned list is the original largest cc size,
    and the k+1 entry is the largest cc size after attackting first k nodes.
    '''   
    resilience_list = [largest_cc_size(ugraph)]
    copy_graph = dict(ugraph)
    for attack_node in attack_order:
        copy_graph.pop(attack_node)
        for node in copy_graph:
            if attack_node in copy_graph[node]:
                copy_graph[node].remove(attack_node)
        resilience_list.append(largest_cc_size(copy_graph))
    return resilience_list

    
    
    