import json
from sklearn.cluster import KMeans
import numpy as np

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

def kmeans(file_name):
    """Generates clusters using kmeans.
    
    Args:
        file_name: The name of the file containing the data that k-means 
        clustering will be run on.

    Returns:
        A list of cluster labels such that the nth element in the list 
        represents the cluster the nth element was placed in. Cluster labels
        are integers.
    """

    with open('./'+str(file_name),"r") as json_file:
        data = json.load(json_file)
    
    data_array = time_series_array(data)

    min_vals = data_array.min(axis=1)
    new_data = [arr-val for arr,val in zip(data_array,min_vals)]

    kmeans = KMeans(n_clusters=7, random_state=0).fit(new_data)

    return kmeans.labels_