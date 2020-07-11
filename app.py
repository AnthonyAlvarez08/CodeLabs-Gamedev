"""
Here is where the web app will run
"""
# import socket, _thread
from flask import Flask, render_template, url_for
from recieveData import JoinCode, HostForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '975c9775521fd39cba0f67c131bdf4b7'

# home page where you will be prompted to host or join a game
@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    # will redirect to host or join depending on what theu choose
    pass


@app.route("/host", methods=["GET", "POST"])
def host():
    pass

@app.route("/join", methods=["GET", "POST"])
def join():
    pass

# shows up while waiting for people to join, will have a "begin" button kind of like kahoot
@app.route("/waiting", methods=["GET", "POST"])
def host_waiting():
    pass


@app.route("/wait", methods=["GET", "POST"])
def player_wait():
    pass


# the playing part of the game
@app.route("/play", methods=["GET", "POST"])
def play():
    pass

if __name__ == "__main__":
    app.run(debug=True)
