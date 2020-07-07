from flask import Flask, render_template
import json
import clustering

# initializes the flask app
app = Flask(__name__)

@app.route("/")
def homepage():
    """"Renders the index page of the app."""
    return render_template("index.html")

@app.route("/data/<file_name>")
def send_data(file_name):
    """Sends the requested file."""
    with open('./'+str(file_name),"r") as json_file:
        data = json.load(json_file)
    return data

@app.route("/K-means/<file_name>")
def kmeans_clustering(file_name):
    """Returns the cluster each time series was placed in.
    
    Args:
        file_name: The name of the file containing the data that k-means 
        clustering is run on. The file must be a json and contain a time
        series object.
    
    Returns:
        A string of the list containing the label of the cluster each time
        series was grouped in.
    """

    labels = clustering.kmeans(str(file_name))
    return str(labels.tolist())

# runs the flask app
if __name__ == "__main__":
    app.run(debug=True)