import graph_generator

############################################
# load graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
network_graph = graph_generator.load_graph(NETWORK_URL)

############################################
# calculate m and n for UPA graph

# n is the number of nodes, n = 1239
# m is the average out_degree, m = 2

# print len(network_graph)

def compute_out_degrees(graph):
    out_degrees = {}
    for node in graph:
        out_degrees[node] = len(graph[node])
    return out_degrees

degrees = compute_out_degrees(network_graph).values()
mean_out_degree = sum(degrees)/(2*len(degrees))
print mean_out_degree

############################################
# calculate p for ER graph

# choose p = 0.004, which the number of edges generated is about 3050

p = 0

def compute_edges(ugraph):
    edge = 0
    for node in ugraph:
        edge += len(ugraph[node])
    return edge / 2

target_edge = 3047
er_graph = graph_generator.ER_undirected(1239, p)
current_edge = compute_edges(er_graph)
while current_edge < target_edge:
    print "current p is", p
    print "current edge numbers", current_edge
    p += 0.001
    er_graph = graph_generator.ER_undirected(1239, p)
    current_edge = compute_edges(er_graph)
print "current p is", p
print "current edge numbers", current_edge
