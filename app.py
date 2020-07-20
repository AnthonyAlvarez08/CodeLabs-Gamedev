"""
Here is where the web app will run
mingjie avialble after 6pm eastern
TODO: rooms, fix uno reverse logic, hook up uno logic to this, rooms
"""
# import socket, _thread
from flask import Flask, render_template, url_for, flash, redirect, request
from recieveData import JoinForm, HostForm
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '975c9775521fd39cba0f67c131bdf4b7'
cors = CORS(app)
socketio = SocketIO(app)

# sample socketio thing to update all clients 
# what happens when people join? how browser know join? front end maybe?
# how does program know what joined means
@socketio.on('join')
def client_connected(person):
    print(f'{person} joined')
    print(request.sid)
    send(person, broadcast=True)


@socketio.on('move')
def handle_move_request(move):
    pass

@socketio.on('connect')
def initialize():
    pass



# # # # # # # # # # # # # # # # # #
# Transition to renediring pages  #
# # # # # # # # # # # # # # # # # #

# home page where you will be prompted to host or join a game
# testing something, not final
@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    # will redirect to host or join depending on what theu choose
    form = HostForm(request.form)
    if form.validate_on_submit():
        flash('Happy gaming :)!')
        redirect(url_for('host'))
    return render_template('home.html', form=form)


@app.route("/host", methods=["GET", "POST"])
def host():
    return 'oof'

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
    socketio.run(app, debug=True)
