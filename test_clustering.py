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
            data, None)
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
            data, None)
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
            data, None)
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

    def test_outliers_simple(self):
        """Should not make any of the cluster labels outliers."""
        data = np.array([[0, 10, 9, 7], [1, 7, 9, 6], [3, 4, 3, 3],
                         [4, 3, 4, 3]])
        ts_cluster_labels = np.array([1, 1, 2, 2])
        cluster_centers = np.array([[0.5, 8.5, 9, 6.5], [3.5, 3.5, 3.5, 3]])
        old = np.copy(ts_cluster_labels)
        clustering.outliers_kmeans(data, ts_cluster_labels, cluster_centers)
        self.assertEqual(ts_cluster_labels.tolist(), old.tolist())

    def test_outliers_update_clusters(self):
        """Should mark some of the time series as outliers."""
        data = np.array([[0, 10, 9, 7], [1, 7, 9, 6], [3, 4, 3, 3],
                         [4, 3, 4, 3]])
        ts_cluster_labels = np.array([1, 1, 2, 2])
        cluster_centers = np.array([[0.5, 0, 9, 2], [3.5, 3.5, 3.5, 3]])
        solution = np.array([-1, -1, 2, 2])
        clustering.outliers_kmeans(data, ts_cluster_labels, cluster_centers)
        self.assertEqual(ts_cluster_labels.tolist(), solution.tolist())

    def test_cluster_medians(self):
        """Should return the cluster medians."""
        data = np.array([[0, 10, 9, 7], [1, 7, 9, 6], [3, 4, 3, 3],
                         [4, 3, 4, 3], [1, 1, 1, 1], [1, 1, 1, 1]])
        cluster_assignment = np.array([0, 0, 1, 1, 2, 2])
        solution = [[0.5, 8.5, 9, 6.5], [3.5, 3.5, 3.5, 3], [1, 1, 1, 1]]
        result, _ = clustering.cluster_medians(data, cluster_assignment)
        self.assertEqual(result.tolist(), solution)

    def test_cluster_medians_order(self):
        """Should return the cluster medians in order."""
        data = np.array([[0, 10, 9, 7], [1, 7, 9, 6], [3, 4, 3, 3],
                         [4, 3, 4, 3]])
        cluster_assignment = np.array([1, 0, 0, 1])
        solution = [[2, 5.5, 6, 4.5], [2, 6.5, 6.5, 5]]
        result, _= clustering.cluster_medians(data, cluster_assignment)
        self.assertEqual(result.tolist(), solution)

    def test_cluster_median_multiple(self):
        """Should return the cluster medians when clusters have more
        than 2 elements."""
        data = np.array([[0, 10, 9, 7], [1, 7, 9, 6], [3, 4, 3, 3],
                         [4, 3, 4, 3], [1, 1, 1, 1]])
        cluster_assignment = np.array([0, 0, 1, 1, 0])
        solution = [[1, 7, 9, 6], [3.5, 3.5, 3.5, 3]]
        result, _ = clustering.cluster_medians(data, cluster_assignment)
        self.assertEqual(result.tolist(), solution)
    def test_add_link_add_index(self):
        """Should add indexes if not in link_dict."""
        must_link = {1: [2, 3], 3: [4, 5], 5: [1, 2]}
        index_1, index_2 = 10, 3
        clustering.add_link(index_1, index_2, must_link)
        solution = {1: [2, 3], 3: [4, 5, 10], 5: [1, 2], 10: [3]}
        self.assertEqual(must_link, solution)

    def test_violates_cons_empty(self):
        """Should return False if there are no constraints."""
        option, ts_index = 2, 3
        ts_to_cluster = must_link = can_not_link = {}
        result = clustering.violates_cons(option, ts_index, ts_to_cluster,
                                          must_link, can_not_link)
        self.assertEqual(False, result)

    def test_violates_cons_false(self):
        """Should return False if must_link matches the option."""
        option, ts_index = 2, 3
        ts_to_cluster = {2: 2}
        must_link = {3: [2], 2: [3]}
        can_not_link = {}
        result = clustering.violates_cons(option, ts_index, ts_to_cluster,
                                          must_link, can_not_link)
        self.assertEqual(False, result)

    def test_violates_cons_multiple_false(self):
        """Should return False if there is no constraint violated."""
        option, ts_index = 2, 3
        ts_to_cluster = {2: 2}
        must_link = {3: [2], 2: [3]}
        can_not_link = {3: [4, 5], 4: [5, 9], 5: [3, 4], 9: [4]}
        result = clustering.violates_cons(option, ts_index, ts_to_cluster,
                                          must_link, can_not_link)
        self.assertEqual(False, result)

    def test_violates_cons_must_true(self):
        """Should return true if a must link constraint is violated."""
        option, ts_index = 2, 3
        ts_to_cluster = {2: 9}
        must_link = {3: [2], 2: [3]}
        can_not_link = {3: [4, 5], 4: [5, 9], 5: [3, 4], 9: [4]}
        result = clustering.violates_cons(option, ts_index, ts_to_cluster,
                                          must_link, can_not_link)
        self.assertEqual(True, result)

    def test_violates_cons_cannot_true(self):
        """Should return true if a cannot link constraint is violated."""
        option, ts_index = 2, 3
        ts_to_cluster = {9: 2}
        must_link = {3: [2], 2: [3]}
        can_not_link = {3: [9], 9:[3]}
        result = clustering.violates_cons(option, ts_index, ts_to_cluster,
                                          must_link, can_not_link)
        self.assertEqual(True, result)

    def test_update_centroids_one_elt(self):
        """Should update the centroids to equal the data elements."""
        data = [[1, 1, 0],
                [1, 1, 1],
                [1, 1, 1],
                [0, 1, 1]]
        clusters = [[0], [3]]
        centroids = np.array([[1, 1, 0], [0, 0, 0]])
        valid = clustering.update_centroids(np.array(data), clusters, centroids)
        result = [[1, 1, 0], [0, 1, 1]]
        self.assertEqual(centroids.tolist(), result)
        self.assertEqual(True, valid)

    def test_update_centroids_false(self):
        """Should return False because one cluster is empty."""
        data = [[1, 1, 0], [0, 0, 0]]
        clusters = [[0], []]
        centroids = np.array([[1, 1, 0], [0, 0, 0]])
        valid = clustering.update_centroids(np.array(data), clusters, centroids)
        self.assertEqual(False, valid)

    def test_update_centroids_multiple(self):
        """Should update centroids to equal the mean."""
        data = [[1, 1, 0],
                [1, 1, 1],
                [0, 1, 1],
                [2, 3, 4]]
        clusters = [[0, 1], [2, 3]]
        centroids = np.array([[1.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
        valid = clustering.update_centroids(np.array(data), clusters, centroids)
        result = [[1, 1, 1/2], [1, 2, 2.5]]
        self.assertEqual(centroids.tolist(), result)
        self.assertEqual(True, valid)

    def test_update_clusters(self):
        """Should update cluster assignment."""
        data = [[1, 1, 0],
                [1, 1, 1],
                [0, 1, 1],
                [2, 3, 4]]
        clusters = [[0, 1], [2, 3]]
        centroids = np.array([[1.0, 1.0, 0.0], [5.0, 2.0, 3.0]])
        clusters, ts_cluster = clustering.update_clusters(data, centroids,
                                                          {}, {})
        result_clusters = [[0, 1, 2], [3]]
        result_assignment = {0: 0, 1: 0, 2: 0, 3: 1}
        self.assertEqual(clusters, result_clusters)
        self.assertEqual(ts_cluster, result_assignment)
    def test_cluster_zone(self):
        """Should assign time series to the label which they have,
        according to ts_to_labels."""
        label_dict = {"north": 0,
                      "south": 1,
                      "west": 2,
                      "east": 3}
        ts_to_labels = np.zeros((5, 4))
        ts_to_labels[0][1] = 1
        ts_to_labels[1][2] = 1
        ts_to_labels[2][0] = 1
        ts_to_labels[3][2] = 1
        ts_to_labels[4][3] = 1

        result = clustering.cluster_zone(label_dict, ts_to_labels)
        solution = ["south", "west", "north", "west", "east"]
        self.assertEqual(result, solution)

if __name__ == '__main__':
    unittest.main()
