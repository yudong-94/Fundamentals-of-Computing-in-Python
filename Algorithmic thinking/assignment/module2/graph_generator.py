# general imports
import urllib2
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
    
##########################################################
# loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

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

##########################################################
# functions to create graphs
def ER_undirected(n, p):
    '''
    for a given number of nodes n, 
    and a probability p,
    retun a directed graph,
    in which any nodes connect to another with probability p
    '''
    nodes = [i for i in range(n)]
    copy_nodes = list(nodes)
    graph = {}
    for node in nodes:
        graph[node] = set([])
    for i in range(len(nodes)):
        current_node = nodes[i]
        for node in copy_nodes:
            if node != current_node:
                a = random.random()
                if a < p:
                   graph[current_node].add(node)
                   graph[node].add(current_node)
        copy_nodes.remove(current_node)
    return graph

# print ER_undirected(10, 0.5)

def make_complete_graph(num_nodes):
    '''
    for the given num_nodes,
    return a complete undirected graph in dictionary
    with all possible edges except self-loop.
    '''
    graph = {}
    complete_set = set([dummy_i for dummy_i in range(num_nodes)])
    if num_nodes > 0:
        for dummy_i in range(num_nodes):
            graph[dummy_i] = complete_set.difference(set([dummy_i]))
    return graph

def UPA(n, m):
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
        for k in connected_nodes:
            graph[k].add(i) 
        #print i, graph[i]
    return graph

# print UPA(10, 3)

