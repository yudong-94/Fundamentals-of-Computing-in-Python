'''
implementation of cloest pair algorithm & 
clustering algorithm
'''

#import alg_cluster
import cluster_class_provided as alg_cluster

def slow_closest_pair(cluster_list):
    '''
    take a list of cluster objects,
    return a closest pair in the form of tuple (dist, idx1, idx2),
    with idx1 < idx2 and dist is the distance between the closest pair
    cluster_list[idx1] and cluster_list[idx2]
    '''
    dist = float("inf")
    idx1 = -1
    idx2 = -1
    for cluster1 in range(len(cluster_list)):
        for cluster2 in range(len(cluster_list)):
            if cluster1 != cluster2:
                current_dist = cluster_list[cluster1].distance(cluster_list[cluster2])
                if current_dist < dist:
                    dist = current_dist
                    idx1 = min(cluster1, cluster2)
                    idx2 = max(cluster1, cluster2)
    return (dist, idx1, idx2)

def fast_closest_pair(cluster_list):
    '''
    take a sorted list of clister objects 
    (sorted in nondecreasing order of their horizontal coordinates),
    return a clostest pair as slow_closest_pair
    '''
    if len(cluster_list) <= 3:
        (dist, idx1, idx2) = slow_closest_pair(cluster_list)
    else:
        middle_length = int(len(cluster_list) / 2)
        left_list = cluster_list[:middle_length]
        right_list = cluster_list[middle_length:]
        (dist_left, idx1_left, idx2_left) = fast_closest_pair(left_list)
        (dist_right, idx1_right, idx2_right) = fast_closest_pair(right_list)
        if dist_left <= dist_right:
            (dist, idx1, idx2) = (dist_left, idx1_left, idx2_left)
        else:
            (dist, idx1, idx2) = (dist_right, idx1_right + middle_length, idx2_right + middle_length)
        mid_x = (cluster_list[middle_length-1].horiz_center() + cluster_list[middle_length].horiz_center()) / 2.0
        closest_strip =  closest_pair_strip(cluster_list, mid_x, dist)
        if closest_strip[0] < dist:
            dist = closest_strip[0]
            idx1 = closest_strip[1]
            idx2 = closest_strip[2]
    return (dist, idx1, idx2)

def closest_pair_strip(cluster_list, horiz_center, half_width):
    '''
    takes a list of cluster objects and two floats, in which
    horiz_center specifies the horizontal position of the center line for a vertical strip,
    half_width specifies the maximal distance of any point in the strip from the center line
    '''
    inrange_clusters = []    
    for cluster in cluster_list:
        if horiz_center - half_width < cluster.horiz_center() < horiz_center + half_width:      
            inrange_clusters.append(cluster)
    inrange_clusters.sort(key = lambda cluster: cluster.vert_center())
    length = len(inrange_clusters)
    dist = float("inf")
    idx1 = -1
    idx2 = -1
    for cluster1 in range(length-1):
        for cluster2 in range(cluster1+1, min(cluster1+3, length-1)+1):
            current_dist = inrange_clusters[cluster1].distance(inrange_clusters[cluster2])
            if current_dist < dist:
                dist = current_dist
                idx1 = cluster_list.index(inrange_clusters[cluster1])
                idx2 = cluster_list.index(inrange_clusters[cluster2])
    return (dist, min(idx1, idx2), max(idx1, idx2))

def hierarchical_clustering(cluster_list, num_clusters):
    '''
    takes a list of cluster object and applies hierarchical clustering,
    proceed until num_clusters clusters remain
    '''
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    while len(cluster_list) > num_clusters:
        closest = fast_closest_pair(cluster_list)
        cluster1 =cluster_list[closest[1]]
        cluster2 =cluster_list[closest[2]]
        cluster_list.append(cluster1.merge_clusters(cluster2))
        cluster_list.remove(cluster1)
        cluster_list.remove(cluster2)
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    return cluster_list

###########testing
#print hierarchical_clustering([alg_cluster.Cluster(set([1, 2]), 0, 0, 1, 1),
#                               alg_cluster.Cluster(set([3, 4]), 0, 1, 2, 1),
#                               alg_cluster.Cluster(set([5, 6]), 0, 1, 3, 1)], 1)


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    '''
    takes a list of cluster objects and applies k-means clustering.
    compute an initial list of clusteres with the property that each cluster
    consists of a single county chosen from the set of the num_cluster countries
    with the largest populations.
    then compute num_iterations of k-means clustering
    and return the resulting list of clusters.
    '''
    length = len(cluster_list)
    copy_cluster_list = list(cluster_list)
    copy_cluster_list.sort(key = lambda cluster: cluster.total_population())
    copy_cluster_list.reverse()
    k_clusters = copy_cluster_list[:num_clusters]
    for dummy_count in range(num_iterations):
        new_cluster_list = []
        for dummy_count in range(num_clusters):
            new_cluster_list.append(alg_cluster.Cluster(set(), 0, 0, 0, 0))
        for county in range(length):
            dist = float("inf")
            for idx in range(num_clusters):
                if k_clusters[idx].distance(copy_cluster_list[county]) < dist:
                    dist = k_clusters[idx].distance(copy_cluster_list[county])
                    target_cluster_idx = idx
            new_cluster_list[target_cluster_idx].merge_clusters(copy_cluster_list[county])
        k_clusters = list(new_cluster_list)
    return new_cluster_list

#print kmeans_clustering([alg_cluster.Cluster(set([1, 2]), 1, 1, 1, 1),
#                         alg_cluster.Cluster(set([3, 4]), 2, 2, 2, 1),
#                         alg_cluster.Cluster(set([5, 6]), 3, 3, 3, 1)], 2, 1)