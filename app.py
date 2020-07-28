"""
Here is where the web app will run
mingjie avialble after 6pm eastern
TODO: rooms, fix uno reverse logic, hook up uno logic to this, rooms
TODO: player class, non generator deck
"""
from flask import Flask, render_template, url_for, flash, redirect, request
from receiveData import JoinForm
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_cors import CORS
from time import time
import time

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = '975c9775521fd39cba0f67c131bdf4b7'
socketio = SocketIO(app)
# for now I am just making it four people per game
Q = []
ROOMS = dict()
inGame=dict()
size = 4


# ROOMS={"roomid":[[player1,F],[player2,F],[player3,F],[player4,F]]}
#inGame={playersid:roomid}

@app.route('/')
def index():
    return render_template('otherindex.html')


@socketio.on('connect')
def on_create():
    send("searching for a room...")
    Q.append(request.sid)
    if len(Q) >= size:
        make_room()

# creates and confirms that players are connected to a room by sending out ready signal
def make_room():
    roomid = str(time.time())
    for i in range(size):
        player = Q.pop(0)
        join_room(roomid, player)
        ROOMS.setdefault(roomid,[])
        ROOMS[roomid].append([player,False])
        emit('join_room', {'user': player}, room=roomid)
        print(player + " has entered the room " + roomid)
        send("are you ready?", room=player)
    socketio.emit('ready', room=roomid)
    #start some sort of countdown

#mega ack confirm user and/ or if all users in a room are ready then starts game
@socketio.on('ready')
def confirm_ready():
    print("received ready signal from "+request.sid)
    send("ready was confirmed! please wait for other players to also confirm")
    val_list=list(ROOMS.values())
    key_list=list(ROOMS.keys())
    i=0

    for val in val_list:
        for v in val:
            if v[0]==request.sid:
                v[1]=True
    for k in key_list:
        for people in (ROOMS.get(k)):
            if people[1]==True:
                i+=1
                if i==size:
                    send("game is starting :D", room=k)
                    move_to_in_game(k)
                    del ROOMS[k]
                    #startGame() function with game code
                    print("game in "+k+ " is starting")
        i=0

@socketio.on('not_ready')
def back_to_queue():
    nrplayer= request.sid
    keys=list(ROOMS.keys())
    room=""
    #find the room that failed to get 4 readys 
    for k in keys:
        players=ROOMS.get(k)
        for player in players:
            if player[0]==nrplayer:
                room=k
                break
        if room!="":
            break
    #for multiple not readys 
    if room=="": 
        return 

    emit('refresh',room=room)
    time.sleep(5)

    players=ROOMS.get(room)
    for player in players: 
        leave_room(room,player[0])
    del ROOMS[room]
   
    

#move ready confirmed users from ROOMS to inGame
def move_to_in_game(ri):#room id
    players=ROOMS[ri]
    for player in players:
        inGame[player[0]]=ri


    
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

while True:
    socketio.on_event('play', None)
    socketio.on_event('draw', None)
    socketio.on_event('+2', None)
    socketio.on_event('+4', None)
    socketio.on_event('skip', None)
    socketio.on_event('reverse', None)
    socketio.on_event('color swap', None)


socketio.to('room').emit('message') is a thing
 
when lobby has 4 players
new room with id = str(time.time())
for player in players: join_room(id)
"""

if __name__ == '__main__':
    socketio.run(app, debug=True)