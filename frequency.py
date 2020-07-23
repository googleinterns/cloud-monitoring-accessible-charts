"""This module contains functions for counting the frequency of elements.
"""

def one_hot_encoding(ts_labels, label_to_index, labels_encoded):
    """Updates labels_encoded based on ts_labels.

    Args:
        ts_labels: Dictionary where a key is a label type and the value
            is the label value.
        label_to_index: Dictionary where a key is a label and the value
            is the index of the label.
        labels_encoded: List where the ith element is a 1 if the time
            series has the label with index i from label_to_index and
            is 0 otherwise.
    """
    for label in ts_labels:
        label_value = ts_labels[label]
        if label_value in label_to_index:
            labels_encoded[label_to_index[label_value]] = 1

def count_labels(ts_labels, label_count):
    """Updates label_count based on ts_labels.

    Args:
        ts_labels: Dictionary where a key is a label type and the value
            is the label value.
        label_count: Dictionary where each key is a label and each
            value is the number of times the label appears in the data.
    """
    for label in ts_labels:
        label_value = ts_labels[label]
        if label_value not in label_count:
            label_count[label_value] = 1
        else:
            label_count[label_value] += 1

def get_dates_labels(data, date_to_index, label_to_count, label_encoding):
    """Updates date_to_index and label_to_count to include all unique
    dates and the count of each unique label, respectively.

    Args:
        data: TimeSeries object.
        date_to_index: Dictionary where each key is a date and each
            value is the index of the date.
        label_to_count: Dictionary where each key is a label and each
            value is the number of times the label appears in the data.
        label_encoding: String indicating how the labels are encoded.
    """
    for time_series in data["timeSeries"]:
        for point in time_series["points"]:
            start_time = point["interval"]["startTime"]
            if start_time not in date_to_index:
                date_to_index[start_time] = len(date_to_index)
        if label_encoding == "one-hot":
            count_labels(time_series["metric"]["labels"], label_to_count)
            count_labels(time_series["resource"]["labels"], label_to_count)
