import json
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def time_series_array(data):
    """Converts the time series data to an np array.

    Args:
        data: A timeSeries object.
    
    Returns:
        An np array where each row represents a resource and each column 
        represents the value at time t.
    """
    num_instances = len(data["timeSeries"])
    # assumes that this instance has all the dates
    num_times = len(data["timeSeries"][0]["points"])
    data_array = [0]*num_instances

    date_to_index = {}
    instance_to_index = {}

    for ts in data["timeSeries"]:
        points = [0]*num_times
        instance_id = ts["resource"]["labels"]["instance_id"]
        instance_to_index[instance_id] = len(instance_to_index)
        for point in ts["points"]:
            if point["interval"]["startTime"] not in date_to_index:
                date_to_index[point["interval"]["startTime"]] = len(date_to_index)
            points[date_to_index[point["interval"]["startTime"]]] = point["value"]["doubleValue"]
        data_array[instance_to_index[instance_id]] = points
    
    return np.array(data_array)

def kmeans(data):
    """Generates clusters using kmeans.
    
    Args:
        data: A timeSeries object.

    Returns:
        A list of cluster labels such that the nth element in the list 
        represents the cluster the nth element was placed in. Cluster labels
        are integers.
    """
    data_array = time_series_array(data)
    scaled_data = [arr-val for arr,val in zip(data_array,data_array.min(axis=1))]

    kmeans = KMeans(n_clusters=7, random_state=0).fit(scaled_data)
    return kmeans.labels_

def dbscan(data):
    """Generates clusters using DBSCAN.
    
    Args:
        data: A timeSeries object.

    Returns:
        A list of cluster labels such that the nth element in the list 
        represents the cluster the nth element was placed in. Cluster labels
        are integers.
    """
    data_array = time_series_array(data)
    scaled_data = [arr-val for arr,val in zip(data_array,data_array.min(axis=1))]

    min_max_scaler = MinMaxScaler()
    min_max_scaled = min_max_scaler.fit_transform(scaled_data)

    # dbscan = DBSCAN(eps=.05, min_samples=1).fit(scaled_data)
    dbscan = DBSCAN(eps=1, min_samples=1).fit(min_max_scaled)
    return dbscan.labels_