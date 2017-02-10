"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import matplotlib.pyplot as plt

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

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
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)

# print citation_graph

###################################
# question 1
# compute in-degree distribution for this citation graph and plot


distribution = in_degree_distribution(citation_graph)
distribution.pop(0)
values = distribution.values()
sum_value = sum(values)
normalized_values = map(lambda i: float(i)/sum_value, values)

plt.loglog(distribution.keys(), normalized_values, "o")
plt.title("Normalized In-degree Distribution")
plt.xlabel("In-degree value")
plt.ylabel("Number of Nodes")
plt.show()



###################################
# question 3
# compute average out_degree

def compute_out_degrees(graph):
    out_degrees = {}
    for node in graph:
        out_degrees[node] = len(graph[node])
    return out_degrees

degrees = compute_out_degrees(citation_graph).values()
mean_out_degree = sum(degrees)/len(degrees)
print mean_out_degree

# n = number of nodes in citation graph = 27770
# m = average out_degrees = 12

        