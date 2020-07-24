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
import time

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = '975c9775521fd39cba0f67c131bdf4b7'
socketio = SocketIO(app)
#for now I am just making it four people per game 
Q=[]
ROOMS=dict() 
size=4
#ROOMS={"roomid":[player1,player2,player3,player4]}

@app.route('/')
def index():
		return render_template('otherindex.html')

@socketio.on('connect')
def on_create():
	Q.append(request.sid)
	if len(Q)>=size:
		make_room()
#creates and confirms that players are connected to a room by sending out ready signal
def make_room():
	roomid=str(time.time())
	for i in range(size):
		player=Q.pop(0)
		join_room(roomid,player)
		emit('join_room', {'user':player}, room=roomid)
		send(player+ " has entered the room " + roomid, room=roomid)
	socketio.emit('ready', room=roomid, callback= ready_to_begin)
	return

#its supposed to be that if the emit receives a signal back it should trigger ready_to_begin as a callback but I don't think i did it right ** 

def ready_to_begin(event):
	print("received ready signal from client")


@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)


"""
#commenting this out for now _ 
# home page where you will be prompted to host or join a game
# testing something, not final
@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
     #will redirect to host or join depending on what theu choose
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
"""
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

if __name__ == '__main__':
	socketio.run(app, debug=True)
