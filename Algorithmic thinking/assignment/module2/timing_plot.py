import attack_generator
import graph_generator
import time
import matplotlib.pyplot as plt

node_size = range(10, 1000, 10)
time_pass_original = []
time_pass_fast = []

for size in node_size:
    UPA_graph = graph_generator.UPA(size, 5)
    start_time = time.clock()
    attack_generator.targeted_order(UPA_graph)
    time_pass_original.append(float(time.clock()) - float(start_time))
    start_time = time.clock()
    attack_generator.fast_targeted_order(UPA_graph)
    time_pass_fast.append(float(time.clock()) - float(start_time))

# print time_pass_original
# print time_pass_fast

plt.plot(node_size, time_pass_original, label="targeted_order timing")
plt.plot(node_size, time_pass_fast, label="fast_targeted_order timing")
plt.title("Timing comparison for two attack order generator (Desktop Python)")
plt.xlabel("number of nodes")
plt.ylabel("timing(seconds)")
plt.legend(loc="upper right")
plt.show()
