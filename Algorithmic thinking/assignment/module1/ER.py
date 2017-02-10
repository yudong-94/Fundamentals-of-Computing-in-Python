# general imports
import random
import matplotlib.pyplot as plt

###################################
# helper functions completed in homework 1

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

###################################
# directed graoh generator ER

def ER(n, p):
    '''
    for a given number of nodes n, 
    and a probability p,
    retun a directed graph,
    in which any nodes connect to another with probability p
    '''
    nodes = [i for i in range(n)]
    graph = {}
    for tail in nodes:
        heads = set([])
        for head in nodes:
            if tail != head:
                a = random.random()
                if a < p:
                    heads = heads.union(set([head]))
        graph[tail] = heads
    return graph

###################################
# question 2
# compute in-degree distribution for a random graph and plot

n = 1000
k = 0.3

distribution = in_degree_distribution(ER(n, k))
distribution.pop(0, "no nodes with 0 in_degree")
values = distribution.values()
sum_value = sum(values)
normalized_values = map(lambda i: float(i)/sum_value, values)

plt.loglog(distribution.keys(), normalized_values, "o")
plt.title("Normalized In-degree Distribution")
plt.xlabel("In-degree value")
plt.ylabel("Number of Nodes")
plt.show()



                

