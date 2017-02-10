import cluster_class_provided as alg_cluster
import clustering_plotting_provided as cluster_plot
import project3_solution
import time
import random
import matplotlib.pyplot as plt

##########Q1

def gen_random_clusters(num_clusters):
    cluster_list = []
    for num in range(num_clusters):
        random_x = random.choice([-1, 1]) * random.random()
        random_y = random.choice([-1, 1]) * random.random()
        new_cluster = alg_cluster.Cluster(set([]), random_x, random_y, 0, 0)
        cluster_list.append(new_cluster)
    return cluster_list

time_pass_slow = []
time_pass_fast = []

for num_clusters in range(2, 201):
    random_cluster_list = gen_random_clusters(num_clusters)
    start_time = time.clock()
    project3_solution.slow_closest_pair(random_cluster_list)
    time_pass_slow.append(float(time.clock()) - float(start_time))
    start_time = time.clock()
    project3_solution.fast_closest_pair(random_cluster_list)
    time_pass_fast.append(float(time.clock()) - float(start_time))

#print time_pass_slow
#print time_pass_fast

plt.plot(range(2, 201), time_pass_slow, label="slow_closest_pair timing")
plt.plot(range(2, 201), time_pass_fast, label="fast_closest_pair timing")
plt.title("Timing comparison for two algorithm to find closest pair (Desktop Python)")
plt.xlabel("size of clusters list")
plt.ylabel("timing(seconds)")
plt.legend(loc="upper left")
plt.show()


##########Q7

def compute_distortion(cluster_list, data_table):
    distortion = 0
    for cluster in cluster_list:
        error = cluster.cluster_error(data_table)
        distortion += error
    return distortion

#example_result = cluster_plot.run_example("DATA_111_URL", 'k', 9, plot=False)
#print compute_distortion(example_result[0], example_result[1])

# distortion for hierarchical clustering is 1.75163886916e+11
# distortion for kmeans clustering is 2.71254226924e+11

##########Q10
distortion_h = []
distortion_k = []

for num_cluster in range(6, 21):
    h_clustering = cluster_plot.run_example("DATA_896_URL", 'h', num_cluster, plot=False)
    distortion_h.append(compute_distortion(h_clustering[0], h_clustering[1]))
    k_clustering = cluster_plot.run_example("DATA_896_URL", 'k', num_cluster, plot=False)
    distortion_k.append(compute_distortion(k_clustering[0], k_clustering[1]))

plt.plot(range(6, 21), distortion_h, label="hierarchical_clustering")
plt.plot(range(6, 21), distortion_k, label="kmeans_clustering")
plt.title("Distortion comparison-896 datasets (Desktop Python)")
plt.xlabel("number of output clusters")
plt.ylabel("Distortion(1e12)")
plt.legend(loc="upper right")
plt.show()
