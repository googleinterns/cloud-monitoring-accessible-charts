import json
from flask import Flask, render_template, jsonify
import clustering

# initializes the flask app
app = Flask(__name__)

@app.route("/")
def homepage():
    """"Renders the index page of the app."""
    return render_template("index.html")

@app.route("/data/<chart_id>")
def send_data(chart_id):
    """Sends the requested file."""
    return load_data(chart_id)

def load_data(chart_id):
    """Tries to load the data. Returns an error message if the file is
    not found, otherwise returns the loaded data."""
    try:
        with open('./data/chart-' + str(chart_id) + ".json", "r") as json_file:
            return json.load(json_file)
    except:
        response = {"success": False, "error": {"type": "FileNotFoundError",
                                                "message": "No such chart"}}
        return response, 404

@app.route("/clustering/<algorithm>/<similarity>/<label_encoding>/<chart_id>")
def cluster(algorithm, similarity, label_encoding, chart_id):
    """Returns the cluster each time series was placed in.

    Args:
        algorithm: The algorithm used for clustering. Must be "K-means"
            or "DBSCAN".
        similarity: The similarity measure used for scaling the data
            before clustering. Must be "Proximity" or "Correlation".
        label_encoding: The method used for encoding the labels. Must
            be "None" or "One-Hot".
        chart_id: The id of the file containing the data that k-means
            clustering is run on.

    Returns:
        A string of the list containing the label of the cluster each
        time series was grouped in.
    """
    data = load_data(chart_id)
    if "timeSeries" not in data:
        return data
    time_series_data, label_dict, ts_to_labels = clustering.time_series_array(
        data)
    time_series_data = clustering.preprocess(time_series_data, label_encoding,
                                             similarity, ts_to_labels)
    if algorithm == "k-means":
        labels = clustering.kmeans(time_series_data)
    elif algorithm == "k-means-constrained":
        labels = clustering.kmeans_constrained(time_series_data, label_dict,
                                               ts_to_labels)
    else:
        labels = clustering.dbscan(time_series_data)
    return str(labels.tolist())

@app.route("/frequency/<algorithm>/<similarity>/<label_encoding>/<chart_id>")
def frequency(similarity, algorithm, label_encoding, chart_id):
    """Runs kmeans and gets the frequencies of labels per time series
    and labels per cluster.

    Args:
        similarity: The similarity measure used for scaling the data
            before clustering. Must be "proximity" or "correlation".
        label_encoding: The method used for encoding the labels. Must
            be "none" or "one-hot".
        chart_id: The id of the file containing the data that k-means
            clustering is run on.

    Returns:
        A json with a list of cluster labels generated by running
        kmeans, an array of labels per time series and an array of
        labels per cluster.

    """
    data = load_data(chart_id)
    if "timeSeries" not in data:
        return data
    time_series_data, label_dict, ts_to_labels = clustering.time_series_array(
        data)
    time_series_data = clustering.preprocess(time_series_data, label_encoding,
                                             similarity, ts_to_labels)
    if algorithm == "k-means":
        labels = clustering.kmeans(time_series_data)
    elif algorithm == "k-means-constrained":
        labels = clustering.kmeans_constrained(time_series_data, label_dict,
                                               ts_to_labels)

    cluster_labels = clustering.cluster_to_labels(labels, ts_to_labels)

    ordered_labels, ordered_clusters, ordered_ts = clustering.sort_labels(
        label_dict, cluster_labels, ts_to_labels)

    return jsonify({"labels": ordered_labels,
                    "ts_labels": ordered_ts.tolist(),
                    "cluster_labels": ordered_clusters.tolist()})

@app.route("/tuning/<algorithm>/<similarity>/<label_encoding>/<chart_id>")
def tune_parameters(algorithm, similarity, label_encoding, chart_id):
    """Returns a list with the results of using different parameters
    for algorithm run on the chart chart_id.

    Args:
        algorithm: The algorithm used for clustering. Must be "k-means"
            or "dbscan".
        similarity: The similarity measure used for scaling the data
            before clustering. Must be "proximity" or "correlation".
        label_encoding: The method used for encoding the labels. Must
            be "None" or "One-Hot".
        chart_id: The id of the file containing the data that k-means
            clustering is run on.
    """
    data = load_data(chart_id)
    if "timeSeries" not in data:
        return data
    time_series_data, _, ts_to_labels = clustering.time_series_array(
        data)
    time_series_data = clustering.preprocess(time_series_data, label_encoding,
                                             similarity, ts_to_labels)
    if algorithm == "k-means":
        distances = clustering.tuning_k(time_series_data)
    else:
        distances = clustering.tuning_eps(time_series_data)
    return str(distances)

@app.route("/<path>")
def invalid_route(path):
    """Catches all invalid routes."""
    response = {"success": False, "error": {"type": "RouteNotFoundError",
                                            "message": "No such route"}}
    return response, 404

# runs the flask app
if __name__ == "__main__":
    app.run(debug=True)
