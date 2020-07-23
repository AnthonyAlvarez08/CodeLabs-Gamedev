"""
Here is where the web app will run
mingjie avialble after 6pm eastern
TODO: rooms, fix uno reverse logic, hook up uno logic to this, rooms
TODO: player class, non generator deck
"""
from flask import Flask, render_template, url_for, flash, redirect, request
from receiveData import JoinForm
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from time import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '975c9775521fd39cba0f67c131bdf4b7'
cors = CORS(app)
socketio = SocketIO(app)


# home page where you will be prompted to host or join a game
# testing something, not final
@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    # will redirect to host or join depending on what theu choose
    form = JoinForm(request.form)
    if form.validate_on_submit():
        flash('Happy gaming :)!')
        redirect(url_for('wait'))
    return render_template('home.html', form=form)


@app.route("/wait", methods=["GET", "POST"])
def wait():
    pass


# the playing part of the game
@app.route("/play", methods=["GET", "POST"])
def play():
    pass


# # # # # # # # # # # # # # # # # #
# Transition to handling sockets  #
# # # # # # # # # # # # # # # # # #

# initialize new connection 
@socketio.on('connected')
def join_lobby(person):
    name = person['username']
    join_room('lobby')
    print(f'{name} joined')

# none of these have to be functions specifically as they can just be events in a loop
# they can be socketio.on_event('signal', function(arg)) as we're using a while loop for the game
@socketio.on('ready')
def ready():
    pass

while True:
    socketio.on_event('play', None)
    socketio.on_event('draw', None)
    socketio.on_event('+2', None)
    socketio.on_event('+4', None)
    socketio.on_event('skip', None)
    socketio.on_event('reverse', None)
    socketio.on_event('color swap', None)

"""
socketio.to('room').emit('message') is a thing
 
when lobby has 4 players
new room with id = str(time.time())
for player in players: join_room(id)

"""

if __name__ == "__main__":
    socketio.run(app, debug=True)
