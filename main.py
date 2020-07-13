from flask import Flask, render_template
import json

# initializes the flask app
app = Flask(__name__)

@app.route("/")
def homepage():
    """"Renders the index page of the app."""
    return render_template("index.html")

@app.route("/data/<chart_id>")
def send_data(chart_id):
    """Sends the requested file."""
    with open('./data/chart-'+str(chart_id)+".json","r") as json_file:
        data = json.load(json_file)
    return data

# runs the flask app
if __name__ == "__main__":
    app.run(debug=True)