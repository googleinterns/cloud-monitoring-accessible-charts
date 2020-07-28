import unittest
import json
import numpy as np
import clustering


class TestClusteringMethods(unittest.TestCase):
    """Tests clustering methods. """

    def test_time_series_array_data(self):
        """Should format the time series data such that np_data has an
        array for each time series, label_dict has labels that occur in
        more than 1 and less than all of the time series, and
        instance_labels has an array for each time series and a column
        for each label in label_dict."""
        with open('./data/chart-100.json', "r") as json_file:
            data = json.load(json_file)

        np_data, label_dict, instance_labels = clustering.time_series_array(
            data)
        solution = [[0, 10],
                    [0, 10],
                    [0, 10],
                    [0, 10]]
        self.assertEqual(np_data.tolist(), solution)
        self.assertEqual(label_dict, {'us-central1-a': 0})
        self.assertEqual(instance_labels.tolist(), [[0], [1], [1], [1]])

    def test_time_series_array_ragged(self):
        """Proberly formats the time series object and fills missing
        data with -1."""
        with open('./data/chart-101.json', "r") as json_file:
            data = json.load(json_file)
        np_data, label_dict, instance_labels = clustering.time_series_array(
            data)
        solution = [[0, -1],
                    [0, 10],
                    [0, 10],
                    [0, 10]]
        self.assertEqual(np_data.tolist(), solution)
        self.assertEqual(label_dict, {'us-central1-a': 0})
        self.assertEqual(instance_labels.tolist(), [[0], [1], [1], [1]])

    def test_preprocess_one_hot_correlation(self):
        """Data should be shifted to 0 and the encoded labeled should be
        appended."""
        with open('./data/chart-101.json', "r") as json_file:
            data = json.load(json_file)
        np_data, label_dict, instance_labels = clustering.time_series_array(
            data)
        result = clustering.preprocess(np_data, "one-hot", "correlation",
                                       instance_labels)
        solution = [[1, 0, 0],
                    [0, 10, 1],
                    [0, 10, 1],
                    [0, 10, 1]]
        self.assertEqual(result.tolist(), solution)

    def test_preprocess_one_hot_proximity(self):
        """Data should have the encoded labels appended."""
        data = [[1.883, 2.9374874, 3.927837, -1],
                [5.282929, -1, 4.28983738, 3.98198],
                [8.982978738, 5.9289227, 0, 3.938383],
                [-1, 3.9998, 4.929278, 4.9389]]
        instance_labels = [[0, 1],
                           [0, 1],
                           [0, 0],
                           [1, 0]]
        result = clustering.preprocess(np.array(data), "one-hot", "proximity",
                                       np.array(instance_labels))
        data = [[1.883, 2.9374874, 3.927837, -1, 0, 1],
                [5.282929, -1, 4.28983738, 3.98198, 0, 1],
                [8.982978738, 5.9289227, 0, 3.938383, 0, 0],
                [-1, 3.9998, 4.929278, 4.9389, 1, 0]]
        self.assertEqual(result.tolist(), data)

    def test_preprocess_none_proximity(self):
        """Data should not be changed."""
        data = [[1.883, 2.9374874, 3.927837, -1],
                [5.282929, -1, 4.28983738, 3.98198],
                [8.982978738, 5.9289227, 0, 3.938383],
                [-1, 3.7988, 4.929278, 4.9389]]
        instance_labels = [[0, 1],
                           [0, 1],
                           [0, 0],
                           [1, 0]]
        result = clustering.preprocess(np.array(data), "none", "proximity",
                                       instance_labels)
        self.assertEqual(result.tolist(), data)

    def test_preprocess_none_correlation(self):
        """Should shift the data to zero."""
        data = [[1.883, 2.9374874, 3.927837, -1],
                [5.282929, -1, 4.28983738, 3.98198],
                [8.982978738, 5.9289227, 0, 3.938383],
                [1, 3.7988, 4.929278, 4.93081]]
        instance_labels = [[0],
                           [0],
                           [0],
                           [0]]
        result = clustering.preprocess(np.array(data), "none", "correlation",
                                       instance_labels)
        solution = [[2.883, 3.9374874, 4.927837, 0],
                    [6.282929, 0, 5.28983738, 4.98198],
                    [8.982978738, 5.9289227, 0, 3.938383],
                    [0, 2.7988, 3.929278, 3.93081]]
        self.assertEqual(result.tolist(), solution)

    def test_scale_to_range_ten_stay(self):
        """Should not change the value."""
        result = clustering.scale_to_range_ten([0.0, 10.0], 7.0)
        self.assertEqual(result, 7)

    def test_scale_to_range_ten_down(self):
        """Should shift the value to fall in the range [0, 10]."""
        result = clustering.scale_to_range_ten([5, 100], 9)
        value = ((4) * 10) / 95
        self.assertAlmostEqual(result, value)

    def test_scale_to_range_ten_up(self):
        """Should shift the value to fall in the range [0, 10]."""
        result = clustering.scale_to_range_ten([-383.44, 7.93839], 1)
        value = ((1 - (-383.44)) * 10) / (7.93839 - (-383.44))
        self.assertAlmostEqual(result, value)

    def test_fill_with_median(self):
        """Missing values (-1) in a time series should be filled with
        the median of the time series."""
        data = [[1.883, 2.9374874, 3.927837, -1],
                [5.282929, -1, 4.28983738, 3.98198],
                [8.982978738, 5.9289227, 0, 3.938383],
                [-1, 3.9998, 4.929278, 4.9389]]
        updated_data = [[1.883, 2.9374874, 3.927837, 2.9374874],
                        [5.282929, 4.28983738, 4.28983738, 3.98198],
                        [8.982978738, 5.9289227, 0, 3.938383],
                        [4.929278, 3.9998, 4.929278, 4.9389]]

        result = clustering.fill_with_median(data)
        self.assertEqual(result, updated_data)

    def test_scale_to_zero_zero(self):
        """Should not change the data."""
        data = [[1.883, 2.9374874, 3.927837, 0],
                [5.282929, 0, 4.28983738, 3.98198],
                [8.982978738, 5.9289227, 0, 3.938383],
                [0, 3.9998, 4.929278, 4.9389]]
        result = clustering.scale_to_zero(np.array(data))
        self.assertEqual(result.tolist(), data)

    def test_scale_to_zero_up_down(self):
        """Should shift rows with minimum negative values up and rows
        with positive minimimum values down."""
        data = [[1.883, 2.9374874, 3.927837, -1],
                [5.282929, 1, 4.28983738, 3.98198],
                [8.982978738, 5.9289227, 0, 3.938383],
                [-1, 3.5998, 4.929278, 4.9389]]
        updated_data = [[2.883, 3.9374874, 4.927837, 0],
                        [4.282929, 0, 3.28983738, 2.98198],
                        [8.982978738, 5.9289227, 0, 3.938383],
                        [0, 4.5998, 5.929278, 5.9389]]
        result = clustering.scale_to_zero(np.array(data))
        self.assertEqual(result.tolist(), updated_data)

    def test_cluster_to_labels_one(self):
        """Should return 1 where all elements in a cluster share a label
        and 0 where none do."""
        cluster_labels = [0, 0, 0, 1]
        resource_label = [[1, 1],
                          [1, 1],
                          [1, 1],
                          [0, 1]]
        result = clustering.cluster_to_labels(cluster_labels, resource_label)
        solution = [[1, 1],
                    [0, 1]]
        self.assertEqual(result.tolist(), solution)

    def test_cluster_to_labels_mixed(self):
        """Should return the percetange of elements in a cluster that
        share a label."""
        cluster_labels = [0, 0, 1, 0, 2]
        resource_label = [[1, 1, 0],
                          [1, 1, 1],
                          [1, 1, 1],
                          [0, 1, 1],
                          [0, 0, 0]]
        result = clustering.cluster_to_labels(cluster_labels, resource_label)
        solution = [[2/3, 1, 2/3],
                    [1, 1, 1],
                    [0, 0, 0]]
        self.assertEqual(result.tolist(), solution)

if __name__ == '__main__':
    unittest.main()
