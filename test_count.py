import unittest
import json
import count

class TestCountMethods(unittest.TestCase):
    """Tests count methods."""

    def test_count_labels_empty(self):
        """Should update the empty dictionary."""
        ts_labels = {"hat": "blue",
                     "cat": "spotted",
                     "car": "blue",
                     "phone": "red",
                     "door": "white"}
        label_to_count = {}
        self.assertEqual(label_to_count, {})

        count.count_labels(ts_labels, label_to_count, None)
        solution = {"blue": 2, "spotted": 1, "red": 1, "white": 1}
        self.assertEqual(label_to_count, solution)

    def test_count_labels_nonempty(self):
        """Should update the non empty dictionary."""
        ts_labels = {"hat": "blue",
                     "cat": "spotted",
                     "car": "blue",
                     "phone": "red",
                     "door": "white"}
        label_to_count = {"blue":3, "green": 2}
        count.count_labels(ts_labels, label_to_count, None)
        solution = {"blue": 5, "green": 2, "spotted": 1, "red": 1, "white": 1}
        self.assertEqual(label_to_count, solution)

    def test_count_labels_key(self):
        """Should only add values that correspond to key."""
        ts_labels = {"hat": "blue",
                     "cat": "spotted",
                     "car": "blue",
                     "door": "white"}
        label_to_count = {}
        self.assertEqual(label_to_count, {})

        count.count_labels(ts_labels, label_to_count, "hat")
        solution = {"blue": 1}
        self.assertEqual(label_to_count, solution)

    def test_count_labels_key_none(self):
        """Should only add values that correspond to keyn in this case
        none should be added."""
        ts_labels = {"hat": "blue",
                     "door": "white"}
        label_to_count = {}
        self.assertEqual(label_to_count, {})

        count.count_labels(ts_labels, label_to_count, "asdf")
        solution = {}
        self.assertEqual(label_to_count, solution)

    def test_one_hot_encoding_all(self):
        """Should update all values in labels_encoded."""
        ts_labels = {"hat": "blue",
                     "cat": "spotted",
                     "car": "blue",
                     "phone": "red",
                     "door": "white"}
        label_to_index = {"blue": 0, "spotted": 1, "red": 2, "white": 3}
        labels_encoded = [0]*len(label_to_index)
        count.one_hot_encoding(ts_labels, label_to_index, labels_encoded)
        self.assertEqual(labels_encoded, [1, 1, 1, 1])

    def test_one_hot_encoding_not_all(self):
        """Should update some values in labels_encoded."""
        ts_labels = {"cat": "spotted",
                     "hat": "blue",
                     "door": "white"}
        label_to_index = {"blue": 0, "spotted": 1, "red": 2, "white":3}
        labels_encoded = [0]*len(label_to_index)
        count.one_hot_encoding(ts_labels, label_to_index, labels_encoded)
        self.assertEqual(labels_encoded, [1, 1, 0, 1])

    def test_one_hot_encoding_nonempty(self):
        """Should update some values in labels_encoded where
        labels_encoded is not initially empty."""
        ts_labels = {"cat": "spotted",
                     "hat": "blue",
                     "door": "red"}
        label_to_index = {"blue": 0, "spotted": 1, "red": 2, "white": 3}
        labels_encoded = [1, 1, 0, 0]
        count.one_hot_encoding(ts_labels, label_to_index, labels_encoded)
        self.assertEqual(labels_encoded, [1, 1, 1, 0])

    def test_get_dates_labels(self):
        """Should update date_to_index, label_to_count, and min_max
        according to the data"""
        with open('./data/chart-102.json', "r") as json_file:
            data = json.load(json_file)
        date_to_index = {}
        label_to_count = {}
        min_max = [13.974581782938913, 13.974581782938913]
        count.get_dates_labels(data, date_to_index, label_to_count, min_max,
                               None)
        date_solution = {"2020-06-26T11:29:00Z": 0,
                         "2020-06-26T11:28:00Z": 1,
                         "2020-06-26T11:27:00Z": 2,
                         "2020-06-22T15:44:00Z": 3,
                         "2020-06-22T15:43:00Z": 4,
                         "2020-06-22T15:42:00Z": 5}
        label_solution = {"gke-demo-default-pool-272cd19c-8mr4": 1,
                          "1575673166315746232": 1,
                          "rnataly-hipstershop": 3,
                          "us-central1-a": 3,
                          "gke-demo-default-pool-272cd19c-rprw": 1,
                          "2191822968372163512": 1,
                          "gke-demo-default-pool-272cd19c-czr1": 1,
                          "2722857393479054264": 1}
        min_max_sol = [0.90215044156545332, 14.905993941792985]
        self.assertEqual(date_to_index, date_solution)
        self.assertEqual(label_to_count, label_solution)
        self.assertEqual(min_max, min_max_sol)

    def test_get_dates_labels_key(self):
        """Should update date_to_index, label_to_count, and min_max
        according to the data and the selected key."""
        with open('./data/chart-102.json', "r") as json_file:
            data = json.load(json_file)
        date_to_index = {}
        label_to_count = {}
        min_max = [13.974581782938913, 13.974581782938913]
        count.get_dates_labels(data, date_to_index, label_to_count, min_max,
                               "zone")
        date_solution = {"2020-06-26T11:29:00Z": 0,
                         "2020-06-26T11:28:00Z": 1,
                         "2020-06-26T11:27:00Z": 2,
                         "2020-06-22T15:44:00Z": 3,
                         "2020-06-22T15:43:00Z": 4,
                         "2020-06-22T15:42:00Z": 5}
        label_solution = {"us-central1-a": 3}
        min_max_sol = [0.90215044156545332, 14.905993941792985]
        self.assertEqual(date_to_index, date_solution)
        self.assertEqual(label_to_count, label_solution)
        self.assertEqual(min_max, min_max_sol)

if __name__ == '__main__':
    unittest.main()
