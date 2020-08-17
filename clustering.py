import json
from statistics import median
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import scale
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import count

# These paramaters where determined by runing tuning_k, tuning_eps and
# tuning_eps_options.
params = {"kmeans_ratio": 20, "kmeans_min": 6, "eps_correlation_none": 2.4,
          "eps_proximity_none": 1.3, "eps_proximity_one-hot": 2.1,
          "eps_correlation_one-hot": 2.7}

def time_series_array(data):
    """Converts the time series data to an np array.

    Args:
        data: A timeSeries object.

    Returns:
        An np array where each row represents a resource and each column
        represents the value at time t, a dictionary mapping each label
        to an index and an np array where each row represents a time series
        and each column represents a label as defined in the label dictionary.
    """
    first_val = data["timeSeries"][0]["points"][0]["value"]["doubleValue"]
    date_to_index, label_to_count, min_max = {}, {}, [first_val, first_val]
    count.get_dates_labels(data, date_to_index, label_to_count, min_max)

    labels = list(filter(lambda k: label_to_count[k] > 2 and label_to_count[k]
                         < len(data["timeSeries"]), label_to_count.keys()))
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

def kmeans(data):
    """Generates clusters using kmeans.

    Args:
        data: A timeSeries object.

    Returns:
        A list of cluster labels such that the nth element in the list
        represents the cluster the nth element was placed in. Cluster
        labels are integers.
    """
    data = scale(data)
    tuning_ratio, tuning_min_clusters = len(data) // 20, 6
    kmeans_result = KMeans(n_clusters=tuning_ratio + tuning_min_clusters,
                           random_state=0).fit(data)
    return kmeans_result.labels_

def dbscan(data, similarity, encoding):
    """Generates clusters using DBSCAN.

    Args:
        data: A timeSeries object.
        similarity: The similarity measure used for scaling the data
            before clustering. Must be "proximity" or "correlation".
        label_encoding: The method used for encoding the labels. Must
            be "none" or "one-hot".

    Returns:
        A list of cluster labels such that the nth element in the list
        represents the cluster the nth element was placed in. Cluster
        labels are integers.
    """
    dbscan_result = DBSCAN(eps=params["eps_"+similarity+"_"+encoding],
                           min_samples=2).fit(data)

    return dbscan_result.labels_

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
