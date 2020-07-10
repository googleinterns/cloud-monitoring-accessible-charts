from flask import Flask, render_template

# initializes the flask app
app = Flask(__name__)

@app.route("/")
def homepage():
    """"Renders the index page of the app."""
    return render_template("index.html")

# runs the flask app
if __name__ == "__main__":
    app.run(debug=True)