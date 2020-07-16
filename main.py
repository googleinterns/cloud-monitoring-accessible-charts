from flask import Flask, render_template
import json
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
    with open('./data/chart-' + str(chart_id) + ".json","r") as json_file:
        data = json.load(json_file)
    return data

@app.route("/clustering/<algorithm>/<similarity>/<chart_id>")
def cluster(algorithm, similarity, chart_id):
    """Returns the cluster each time series was placed in.
    
    Args:
        algorithm: The algorithm used for clustering. Must be "K-means"
            or "DBSCAN".
        similarity: The similarity measure used for scaling the data 
            before clustering. Must be "Proximity" or "Correlation".
        chart_id: The id of the file containing the data that k-means 
            clustering is run on.
    
    Returns:
        A string of the list containing the label of the cluster each 
        time series was grouped in.
    """
    with open('./data/chart-' + str(chart_id) + ".json","r") as json_file:
        data = json.load(json_file)
    time_series_data = clustering.time_series_array(data)
    
    if algorithm.lower() == "k-means":
        labels = clustering.kmeans(time_series_data, similarity)
    else:
        labels = clustering.dbscan(time_series_data, similarity)
    return str(labels.tolist())

@app.route("/tuning/<algorithm>/<chart_id>")
def tune_parameters(algorithm, chart_id):
    """Returns a list with the results of using different parameters 
    for algorithm run on the chart chart_id.
    """
    with open('./data/chart-' + str(chart_id) + ".json","r") as json_file:
        data = json.load(json_file)

    if algorithm.lower() == "k-means":
        distances = clustering.tuning_k(data)
    else:
        distances = clustering.tuning_eps(data)
    return str(distances)

# runs the flask app
if __name__ == "__main__":
    app.run(debug=True)