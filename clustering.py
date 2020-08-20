import json
from statistics import median
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import scale
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise_distances, pairwise_distances_argmin_min
from sklearn.metrics import pairwise_distances_argmin
from scipy.spatial import distance
from sklearn.decomposition import PCA
import count

# These params where determined by testing various k, eps produced by running
# tuning_k and tuning_eps respectively, and picking the parameters that were at
# the curve for their respective functions and produced reasonable clusters.
KMEANS_RATIO = 20
KMEANS_MIN = 6
DBSCAN_EPS = 1.2

# These paramaters where determined by runing tuning_k, tuning_eps and
# tuning_eps_options.
# params = {"kmeans_ratio": 20, "kmeans_min": 6, "eps_correlation_none": 2.4,
#           "eps_proximity_none": 1.3, "eps_proximity_one-hot": 2.1,
#           "eps_correlation_one-hot": 2.7}

EPS_CORRELATION_NONE = 2.4
EPS_PROXIMITY_NONE = 1.3
EPS_PROXOMITY_ONE_HOT = 2.1
EPS_CORRELATION_ONE_HOT = 2.7

# It is common to reinitialize the centroids for k-means 10 times.
NUM_RUNS = 10

def time_series_array(data, key):
    """Converts the time series data to an np array.

    Args:
        data: A timeSeries object.
        key: The key for the time series labels that are saved. If None,
            then all label values may be kept, otherwise only label
            values with that key are kept.

    Returns:
        An np array where each row represents a resource and each column
        represents the value at time t, a dictionary mapping each label
        to an index and an np array where each row represents a time series
        and each column represents a label as defined in the label dictionary.
    """
    first_val = data["timeSeries"][0]["points"][0]["value"]["doubleValue"]
    date_to_index, label_to_count, min_max = {}, {}, [first_val, first_val]
    count.get_dates_labels(data, date_to_index, label_to_count, min_max, key)
    if not key:
        labels = list(filter(lambda k: label_to_count[k] >= 2 and
                             label_to_count[k] < len(data["timeSeries"]),
                             label_to_count.keys()))
    else:
        labels = list(label_to_count.keys())
    label_to_index = dict(zip(labels, range(len(labels))))
    num_instances = len(data["timeSeries"])
    num_times = len(date_to_index)
    data_array = [0]*num_instances
    instance_labels = [0]*num_instances

    for index, time_series in enumerate(data["timeSeries"]):
        points = [-1]*num_times
        for point in time_series["points"]:
            start_time = point["interval"]["startTime"]
            points[date_to_index[start_time]] = scale_to_range_ten(
                min_max, point["value"]["doubleValue"])
        data_array[index] = points

        encoding = [0]*len(label_to_index)
        count.one_hot_encoding(time_series["metric"]["labels"],
                               label_to_index, encoding)
        count.one_hot_encoding(time_series["resource"]["labels"],
                               label_to_index, encoding)
        instance_labels[index] = encoding

    return np.array(data_array), label_to_index, np.array(instance_labels)

def scale_to_range_ten(min_max, element):
    """Scale element to the new range, [0,10].

    Args:
        min_max: Original range of the data, [min,max].
        element: Integer that will be scaled to the new range, must be
            within the old_range.

    Returns:
        element scaled to the new range.
    """
    new_range = 10
    old_range = min_max[1] - min_max[0]
    return  ((element - min_max[0]) * new_range) / old_range

def fill_with_median(data):
    """Fills missing values (-1) in a time series to the median of the
    time series.

    Args:
        data: A list where each row is a resource and each column is a
        time.
    """
    data_array = data
    for row in data_array:
        med = median(list(filter(lambda elt: elt != -1, row)))
        for i, val in enumerate(row):
            if val == -1:
                row[i] = med
    return data_array

def preprocess(data, label_encoding, similarity, ts_to_labels, algorithm):
    """Updates the data according to label_encoding and similarity.

    Args:
        data: Array where each row is a time series and each column is
            a date.
        label_encoding: The method used for encoding the labels. Must
            be "none" or "one-hot".
        similarity: The similarity measure used for scaling the data
            before clustering. Must be "proximity" or "correlation".
        ts_to_labels: Array where each row is a time series and each
            column is a label.
        algorithm: The algorithm that will be run on data.

    Returns:
        An np array updated according to label_encoding, similarity and
        algorithm.
    """
    updated_data = data
    if similarity == "correlation":
        updated_data = scale_to_zero(updated_data)
    if algorithm == "dbscan":
        if similarity == "correlation":
            pca = PCA(n_components=.75)
        elif similarity == "proximity":
            pca = PCA(n_components=.85)
        pca.fit(updated_data)
        updated_data = pca.transform(updated_data)
    if label_encoding == "one-hot":
        updated_data = np.concatenate((updated_data, ts_to_labels), axis=1)
    return updated_data

def scale_to_zero(data):
    """Scales the data such that the minimum of each time series is at
    zero.

    Args:
        data: A timeSeries object.

    Returns:
        An np array of the scaled data.
    """
    min_data = np.min(data)
    scaled_data = [arr - abs(min_data - val) for arr, val in zip(
        data, data.min(axis=1))]
    return scaled_data + abs(min_data)

def tuning_k(data):
    """Runs k-means clustering with different values of k and creates a
    list of the sum distances of samples to their cluster center.

    Args:
        data: A timeSeries object.

    Returns:
        A list where the nth entry represents the sum of squared
        distances of samples to their cluster center when k-means is
        run with k set to n+1.
    """
    distances = []
    data = scale(data)
    for i in range(1, len(data) // 2):
        kmeans_result = KMeans(n_clusters=i, random_state=0).fit(data)
        distances.append(kmeans_result.inertia_)
    return distances

def tuning_eps(data):
    """Runs nearest neighbors to identify the distance of the closest
    neighbor of each time series.

    Args:
        data: A timeSeries object.

    Returns:
        A sorted list of the distance of each time series to its
        closest neighbor.
    """
    neighbors = NearestNeighbors(n_neighbors=2)
    fitted = neighbors.fit(data)
    distances, _ = fitted.kneighbors(data)
    return (np.sort(distances[:, 1])).tolist()

def tuning_eps_options(data, start, end, min_clusters):
    """Returns a list of tuples (num_outliers, num_clusters, eps) such
    that runing dbscan with each eps results in more than min_clusters.
    The options are sorted according to the number of oulliers produced.

    Args:
        data: An array where each row is a time series and each column
            is a date.
        start: Smallest eps that is tested.
        end: Largest eps that is tested.
        min_clusters: The minimum number of clusters that should be
            produced by dbscan.

    Returns:
        A list of tuples where each tuple has num_outliers, num_clusters,
        and eps.
    """
    ops = []
    while start <= end:
        dbscan_result = DBSCAN(eps=start, min_samples=2).fit(data)
        num_outliers = len(np.where(dbscan_result.labels_ == -1)[0])
        num_clusters = len(np.unique(dbscan_result.labels_))
        if num_clusters > min_clusters:
            ops.append((num_outliers, num_clusters, start))
        start += 0.1
    ops.sort()
    return ops

def kmeans(data, outlier):
    """Generates clusters using kmeans.

    Args:
        data: A timeSeries object.
        outlier: Indicates whether outliers are labeled as outliers.

    Returns:
        A list of cluster labels such that the nth element in the list
        represents the cluster the nth element was placed in. Cluster
        labels are integers.
    """
    data = scale(data)
    tuning_ratio = len(data) // KMEANS_RATIO
    kmeans_result = KMeans(n_clusters=tuning_ratio + KMEANS_MIN,
                           random_state=0).fit(data)
    labels = np.copy(kmeans_result.labels_) + 1
    if outlier == "on":
        outliers_kmeans(data, labels, kmeans_result.cluster_centers_)
    return labels

def dbscan(data, similarity, encoding, outlier):
    """Generates clusters using DBSCAN.

    Args:
        data: A timeSeries object.
        similarity: The similarity measure used for scaling the data
            before clustering. Must be "proximity" or "correlation".
        label_encoding: The method used for encoding the labels. Must
            be "none" or "one-hot".
        outlier: Indicates whether outliers are labeled as outliers.

    Returns:
        A list of cluster labels such that the nth element in the list
        represents the cluster the nth element was placed in. Cluster
        labels are integers.
    """
    if similarity == "correlation" and encoding == "none":
        eps_tuned = EPS_CORRELATION_NONE
    elif similarity == "correlation" and encoding == "one-hot":
        eps_tuned = EPS_CORRELATION_ONE_HOT
    elif encoding == "none":
        eps_tuned = EPS_PROXIMITY_NONE
    else:
        eps_tuned = EPS_PROXOMITY_ONE_HOT

    dbscan_result = DBSCAN(eps=eps_tuned, min_samples=2).fit(data)
    cluster_assignment = np.copy(dbscan_result.labels_)
    medians = cluster_medians(data, cluster_assignment)

    outlier_indexes = np.where(cluster_assignment == -1)[0]
    cluster_assignment += 1
    closest = pairwise_distances_argmin(data[outlier_indexes, :], medians)

    for index, index_ts in enumerate(outlier_indexes):
        if outlier == "on":
            cluster_assignment[index_ts] = - (closest[index] + 1)
        else:
            cluster_assignment[index_ts] = closest[index] + 1
    return cluster_assignment

def cluster_medians(data, cluster_assignment):
    """Calculates the cluster medians based on the cluster_assignment.

    Args:
        data: Array where each row is a time series and each column is
            a date.
        cluster_assignment: An array of cluster labels where the nth
        element is the cluster the nth time series was placed in.

    Returns:
        An array where the nth element is the median of the nth cluster.
    """
    clusters = {}

    for index in np.where(cluster_assignment >= 0)[0]:
        label = cluster_assignment[index]
        if label not in clusters:
            clusters[label] = [data[index]]
        else:
            clusters[label] = np.append(clusters[label], [data[index]], axis=0)
    medians = [np.median(clusters[i], axis=0) for i in range(len(clusters))]
    return np.array(medians)

def cluster_to_labels(cluster_labels, resource_to_label):
    """Returns a list of the percentage of elements in a cluster that
    share the same label.

    Args:
        cluster_labels: An array where the ith element indicates what
            cluster the ith time series was assigned to.
        resource_to_label: An array where entry [i][j] is a 0 if time
            series i had the label with index j.

    Returns:
        A 2d list where each entry [i][j] represents the percentage of
        time series in cluster i that have label j.
    """
    cluster_count = {}
    for label in cluster_labels:
        if label not in cluster_count:
            cluster_count[label] = 1
        else:
            cluster_count[label] += 1

    ordered_cluster_count = sorted(cluster_count.items(), key=lambda x: x[0])
    values = [x[1] for x in ordered_cluster_count]
    cluster_to_label = np.zeros((len(cluster_count), len(resource_to_label[0])))

    for index, element in enumerate(cluster_labels):
        cluster_to_label[element] += resource_to_label[index]
    return np.multiply(cluster_to_label.T, 1/np.array(values)).T

def sort_labels(label_dict, cluster_labels, ts_to_labels):
    """Returns a list of the sorted labels, an np array of clusters to
    labels, and an np array of time series to labels. In the np arrays,
    the columns are sorted according to the sorted labels.

    Args:
        cluster_labels: An array where each row is a cluster and each
            column is a label.
        label_dict: A dictionary where each key is a system label and
            each value is the index of the label in cluster_labels and
            ts_to_labels.
        ts_to_labels: An array where each row is a time series and each
            column is a label.
    """
    system_labels = list(label_dict.keys())

    ordered = np.argsort(np.array(system_labels))
    ordered_labels = [0]*len(system_labels)
    ordered_ts_labels = np.zeros(ts_to_labels.shape)
    ordered_cluster_labels = np.zeros(cluster_labels.shape)

    for i, elt in enumerate(ordered):
        ordered_ts_labels[:, i] = ts_to_labels[:, elt]
        ordered_cluster_labels[:, i] = cluster_labels[:, elt]
        ordered_labels[i] = system_labels[elt]

    return ordered_labels, ordered_cluster_labels, ordered_ts_labels

def outliers_kmeans(data, ts_cluster_labels, cluster_centers):
    """Updates ts_cluster_labels to reflect whether a time series is an
    outlier in the cluster it was assigned to. '-n' indicates an outlier
    in cluster n.

    Args:
        data: Array where each row is a time series and each column is
            a date.
        ts_cluster_labels: Array where the ith element is the cluster
            the ith time series was placed in.
        cluster_centers: The centroids that were outputted when the
            clustering algorithm was run.
    """
    for index, label in enumerate(ts_cluster_labels):
        euc_dist = distance.euclidean(data[index], cluster_centers[label - 1])
        if euc_dist > 6.75:
            ts_cluster_labels[index] = -label

def kmeans_constrained(data, label_dict, ts_to_labels, outlier):
    """Runs k-means with constraints and uses k-means++ initialization.

    Args:
        data: An np array where each row is a time series and each
            column is a time.
        label_dict: A dictionary where the keys are labels and the
            values are the indexes of the labels in data.
        ts_to_labels: An array where each row is a timeSeries and each
            column is a label.
        outlier: Indicates whether outliers are labeled as outliers.

    Returns:
        An np array where the ith element is the cluster the ith time
        series was placed in.
    """
    must_link, can_not_link = make_constraints(ts_to_labels)
    num_clusters = (len(data) // KMEANS_RATIO) + KMEANS_MIN
    clusters_distances = []

    for run_num in range(NUM_RUNS):
        centroids = k_means_init(data, num_clusters, run_num)

        while True:
            old_centroids = centroids.copy()

            clusters, ts_to_cluster = update_clusters(data, centroids,
                                                      must_link, can_not_link)
            valid_clusters = update_centroids(data, clusters, centroids)

            if not valid_clusters:
                break

            if np.array_equal(old_centroids, centroids):
                assignment = [v for k, v in sorted(ts_to_cluster.items(),
                                                   key=lambda item: item[0])]
                center_dist = 0
                for index, cluster in enumerate(assignment):
                    center_dist += distance.euclidean(data[index],
                                                      centroids[cluster])
                clusters_distances.append([center_dist, assignment, centroids])
                break

    clusters_distances.sort()
    result =  np.array(clusters_distances[0][1]) + 1
    if outlier == "on":
        outliers_kmeans(data, result, clusters_distances[0][2])
    return result

def update_clusters(data, centroids, must_link, can_not_link):
    """Updates the cluster assignments based on the centroids and the
    must_link and can_not_link constraints. Assigns each time series
    to the closest centroid which does not violate the constraints.

    Args:
        data: An np array where each row is a time series and each
            column is a time.
        centroids: A list of the centroids.
        must_link: A dictionary mapping time series that must link.
        can_not_link: A dictionary mapping time series that can't link.

    Returns:
        clusters: A list where the ith element is a list of the indexes
            of the elements in the ith cluster.
        ts_to_cluster: A dictionary mapping each time series to its
            cluster assignment.
    """
    distances_ts_to_cluster = pairwise_distances(data, centroids)
    clusters = [[] for i in range(len(centroids))]
    ts_to_cluster = {}

    for ts_index, dist in enumerate(distances_ts_to_cluster):
        options = np.argsort(dist)
        for option in options:
            invalid = violates_cons(option, ts_index, ts_to_cluster,
                                    must_link, can_not_link)
            if not invalid:
                ts_to_cluster[ts_index] = option
                clusters[option].append(ts_index)
                break
    return clusters, ts_to_cluster

def update_centroids(data, clusters, centroids):
    """Updates the centroids based on the elements in each cluster.

    Args:
        data: An np array where each row is a time series and each
            column is a time.
        clusters: A list where the ith element is a list of the indexes
            of the elements in the ith cluster.
        centroids: A list of the centroids.

    Returns:
        True if the centroids were updated without an error, False
        otherwise.
    """
    for cluster_ind, _ in enumerate(centroids):
        if len(clusters[cluster_ind]) == 0:
            return False
        total = np.zeros((centroids.shape[1]))
        for ts_index in clusters[cluster_ind]:
            total += data[ts_index]
        centroids[cluster_ind] = total / len(clusters[cluster_ind])
    return True

def k_means_init(data, num_clusters, run_num):
    """Runs k-means++ initialization which aims to spread out the
    cluster centroids.

    Args:
        data: An np array where each row is a time series and each
            column is a time.
        num_clusters: The number of clusters.
        run_num: The number of times k-means has been reinitialized. It
            is used as the seed for np.random.seed.

    Returns:
        An np array where the ith element is the ith cluster centroid.
    """
    np.random.seed(run_num)
    num_ts = len(data)
    first = int(num_ts * .2)
    centroids = np.array([data[first]])

    for _ in range(num_clusters -1):
        _, distances = pairwise_distances_argmin_min(data, centroids)
        choices = np.random.choice(num_ts, 1, p=distances/np.sum(distances))
        picked = choices[0]
        centroids = np.append(centroids, [data[picked]], axis=0)
    return centroids

def violates_cons(option, ts_1, ts_to_cluster, must_link, can_not_link):
    """Checks if any constraint is violated by placing ts_1 in the
    cluster option.

    Args:
        option: The index of the cluster where the time series ts_1
            may be placed.
        ts_1: The time series being placed.
        ts_to_cluster: A dictionary where each key is a time series
            index and each value is the index of the cluster the time
            series is assigned to.
        must_link: A dictionary where each key is a time series index
            and each value is a list of time series indexes which must
            be in the same cluster.
        can_not_link: A dictionary where each key is a time series index
            and each value is a list of time series indexes which can
            not be in the same cluster as the key.

    Returns:
        True if a constraint was violated and False otherwise.
    """
    if ts_1 in must_link:
        for ts_2 in must_link[ts_1]:
            if ts_2 in ts_to_cluster and ts_to_cluster[ts_2] != option:
                return True
    if ts_1 in can_not_link:
        for ts_2 in can_not_link[ts_1]:
            if ts_2 in ts_to_cluster and ts_to_cluster[ts_2] == option:
                return True
    return False

def make_constraints(ts_to_labels):
    """Makes must link and can not link constraints. Uses ts_to_labels
    to get the unique time series label combinations and makes the
    constraints based on the label similarity of the time series.

    Args:
        ts_to_labels: An array where each row is a time series and each
            column is a label.

    Returns:
        must_link: A dictionary mapping time series that must link.
        can_not_link: A dictionary mapping time series that can't link.

    """
    np.random.seed(0)
    must_link, can_not_link = {}, {}

    limit = len(ts_to_labels) * .03
    unique_label_patterns = np.unique(ts_to_labels, axis=0)
    pattern_to_rows = {}
    greater_than_limit = []

    for index, row in enumerate(unique_label_patterns):
        ts_indexes = np.where(np.all(ts_to_labels == row, axis=1))[0]
        pattern_to_rows[index] = ts_indexes
        if len(ts_indexes) > limit:
            greater_than_limit.append(index)

    for pattern, indexes in pattern_to_rows.items():
        index_1 = np.random.choice(indexes, 1)[0]
        sec_pattern = np.random.choice(greater_than_limit, 1)[0]
        index_2 = np.random.choice(pattern_to_rows[sec_pattern], 1)[0]
        if pattern != sec_pattern:
            add_link(index_1, index_2, can_not_link)
        else:
            add_link(index_1, index_2, must_link)

    return must_link, can_not_link

def add_link(index_1, index_2, link_dict):
    """Adds a link from index_1 to index_2 and index_2 to index_1.

    Args:
        index_1: Index of the first element.
        index_2: Index of the second element.
        link_dict: Dictionary where each key is an element index and
            each value is a list of element indexes for which the key
            has a link.
    """
    if index_1 in link_dict:
        link_dict[index_1].append(index_2)
    if index_2 in link_dict:
        link_dict[index_2].append(index_1)
    if index_1 not in link_dict:
        link_dict[index_1] = [index_2]
    if index_2 not in link_dict:
        link_dict[index_2] = [index_1]

def cluster_zone(label_dict, ts_to_labels):
    """Clusters the time series based on their zone label.

    Args:
        label_dict: A dictionary where each key is a system label and
            each value is the index of the label (column) in
            ts_to_labels. All keys are zone keys.
        ts_to_labels: An array where each row is a time series and each
            column is a label.

    Returns:
        A list where the ith entry is the name of the cluster the ith
        time series was placed in."""
    index_to_label = dict((v, k) for k, v in label_dict.items())
    labels = [0] * ts_to_labels.shape[0]
    zone_label = np.argwhere(ts_to_labels)
    for ts_index, zone_index in zone_label:
        labels[ts_index] = index_to_label[zone_index]
    return labels
