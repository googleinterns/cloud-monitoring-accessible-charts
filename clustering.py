import json
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import random

def time_series_array(data):
    """Converts the time series data to an np array.

    Args:
        data: A timeSeries object.
    
    Returns:
        An np array where each row represents a resource and each 
        column represents the value at time t.
    """
    date_to_index = {}
    for index,ts in enumerate(data["timeSeries"]):
        for point in ts["points"]:
            start_time = point["interval"]["startTime"]
            if start_time not in date_to_index:
                date_to_index[start_time] = len(date_to_index)
    
    num_instances = len(data["timeSeries"])
    num_times = len(date_to_index)
    data_array = [0]*num_instances

    for index,ts in enumerate(data["timeSeries"]):
        points = [-1]*num_times
        for point in ts["points"]:
            start_time = point["interval"]["startTime"]
            points[date_to_index[start_time]] = point["value"]["doubleValue"]
        data_array[index] = points
    return np.array(data_array)

def scale_to_zero(data):
    """Scales the data such that the minimum of each time series is at 
    zero.
    
    Args:
        data: A timeSeries object.
    
    Returns: 
        An np array of the scaled data.
    """
    data_array = time_series_array(data)
    min_data = np.min(data_array)
    scaled_data = [arr - abs(min_data - val) for arr,val in zip(data_array,
        data_array.min(axis=1))]
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
    scaled_data = scale_to_zero(data)
    distances = []

    for i in range(1, len(scaled_data) // 2):
        kmeans = KMeans(n_clusters=i, random_state=0).fit(scaled_data)
        distances.append(kmeans.inertia_)
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
    scaled_data = scale_to_zero(data)
    min_max_scaler = MinMaxScaler()
    min_max_scaled = min_max_scaler.fit_transform(scaled_data)

    neighbors = NearestNeighbors(n_neighbors=2)
    fitted = neighbors.fit(min_max_scaled)
    distance, index = fitted.kneighbors(min_max_scaled)

    return (np.sort(distance[:,1])).tolist()

def kmeans(data, similarity):
    """Generates clusters using kmeans.
    
    Args:
        data: A timeSeries object.
        similarity: The similarity measure used for scaling the data 
            before clustering. Must be "Proximity" or "Correlation".

    Returns:
        A list of cluster labels such that the nth element in the list 
        represents the cluster the nth element was placed in. Cluster 
        labels are integers.
    """
    if similarity == "Correlation":
        data = scale_to_zero(data)
    tuning_ratio, tuning_min_clusters = len(data) // 16, 8
    kmeans = KMeans(n_clusters = tuning_ratio + tuning_min_clusters, 
        random_state = 0).fit(data)
    return kmeans.labels_

def dbscan(data, similarity):
    """Generates clusters using DBSCAN.
    
    Args:
        data: A timeSeries object.
        similarity: The similarity measure used for scaling the data 
            before clustering. Must be "Proximity" or "Correlation".
    Returns:
        A list of cluster labels such that the nth element in the list 
        represents the cluster the nth element was placed in. Cluster 
        labels are integers.
    """
    if similarity == "Correlation":
        data = scale_to_zero(data)

    min_max_scaler = MinMaxScaler()
    min_max_scaled = min_max_scaler.fit_transform(data)
    dbscan = DBSCAN(eps=1.2, min_samples=1).fit(min_max_scaled)
    return dbscan.labels_