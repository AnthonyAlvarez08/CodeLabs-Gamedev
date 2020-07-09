"""
Here is where the web app will run
"""
from flask import Flask, render_template, url_for
app = Flask(__name__)
app.config['SECRET_KEY'] = '975c9775521fd39cba0f67c131bdf4b7'

# home page where you will be prompted to host or join a game
@app.route("/")
def home():
    pass

if __name__ == "__main__":
    app.run(debug=True)