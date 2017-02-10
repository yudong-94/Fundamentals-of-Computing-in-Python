import BFS
import graph_generator
import attack_generator
import matplotlib.pyplot as plt

'''
##################Q1#######################
# compute resilience

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
network_graph = graph_generator.load_graph(NETWORK_URL)
attack_order_original = attack_generator.random_order(network_graph)
resilience_original = BFS.compute_resilience(network_graph,attack_order_original)

UPA_network = graph_generator.UPA(1239, 2)
attack_order_upa = attack_generator.random_order(UPA_network)
resilience_upa = BFS.compute_resilience(UPA_network,attack_order_upa)


ER_network = graph_generator.ER_undirected(1239, 0.004)
attack_order_er = attack_generator.random_order(ER_network)
resilience_er = BFS.compute_resilience(ER_network,attack_order_er)

############################################
# plotting

plt.plot(range(len(network_graph)+1), resilience_original, label="computer network")
plt.plot(range(len(network_graph)+1), resilience_upa, label="UPA network(n=1239, m=2)")
plt.plot(range(len(network_graph)+1),resilience_er, label="ER network(n=1239, p=0.004)")
plt.title("computer resillience diagram")
plt.xlabel("number of attacked computer")
plt.ylabel("size of the largest connect component")
plt.legend(loc="upper right")
plt.show()
'''

##################Q4#######################
# compute resilience

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
network_graph = graph_generator.load_graph(NETWORK_URL)
attack_order_original = attack_generator.fast_targeted_order(network_graph)
resilience_original = BFS.compute_resilience(network_graph,attack_order_original)

UPA_network = graph_generator.UPA(1239, 2)
attack_order_upa = attack_generator.fast_targeted_order(UPA_network)
resilience_upa = BFS.compute_resilience(UPA_network,attack_order_upa)


ER_network = graph_generator.ER_undirected(1239, 0.004)
attack_order_er = attack_generator.fast_targeted_order(ER_network)
resilience_er = BFS.compute_resilience(ER_network,attack_order_er)

############################################
# plotting

plt.plot(range(len(network_graph)+1), resilience_original, label="computer network")
plt.plot(range(len(network_graph)+1), resilience_upa, label="UPA network(n=1239, m=2)")
plt.plot(range(len(network_graph)+1),resilience_er, label="ER network(n=1239, p=0.004)")
plt.title("computer resillience diagram")
plt.xlabel("number of attacked computer")
plt.ylabel("size of the largest connect component")
plt.legend(loc="upper right")
plt.show()