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
# directed graoh generator DPA

def DPA(n, m):
    '''
    n is the final number of nodes,
    m is the number of existing nodes to which a new node is connected to.
    1 <= m <= n
    '''
    total_set = [node for node in range(m) for i in range(m)]
    graph = make_complete_graph(m)
    # print graph
    for i in range(m, n):
        connected_nodes = set()
        for j in range(m):     
            connected_nodes.add(random.choice(total_set)) 
        total_set.append(i)
        total_set.extend(list(connected_nodes))
        graph[i] = connected_nodes
        #print i, graph[i]
    return graph

dpa_graph = DPA(28000, 12)

print 'graph generated'


distribution = in_degree_distribution(dpa_graph)
distribution.pop(0)
values = distribution.values()
sum_value = sum(values)
normalized_values = map(lambda i: float(i)/sum_value, values)

plt.loglog(distribution.keys(), normalized_values, "o")
plt.title("Normalized In-degree Distribution (DPA)")
plt.xlabel("In-degree value")
plt.ylabel("Number of Nodes")
plt.show()

