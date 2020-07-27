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
from recieveData import JoinForm
import time
from unoClasses import Player, Card

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
                    print(ROOMS)
                    print(inGame)
                    #startGame() function with game code
                    print("game in "+k+ " is starting")
        i=0

@socketio.on('not_ready')
def back_to_queue():
    print("q time")

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


# # # # # # # # # # # # # # # # # # # # # #
# Transition to handling sockets and game #
# # # # # # # # # # # # # # # # # # # # # #

# initialize new connection 
@socketio.on('connected')
def join_lobby(person):
    name = person['username']
    # if not name in room.users: 
    join_room('lobby')
    print(f'{name} joined')



socketio.to('room').emit('message') is a thing
 
when lobby has 4 players
new room with id = str(time.time())
for player in players: join_room(id)
"""


# none of these have to be functions specifically as they can just be events in a loop
# they can be socketio.on_event('signal', function(arg)) as we're using a while loop for the game
@socketio.on('ready')
def ready():
    pass

# variables to iterate through turns
f = 0
increment = 1
poolCard = None

# the front end 
def process_move(card):
    global f; global increment; global poolCard

    if card.isAction:
        if card.action == 'skip':
            if increment == 1:
                if f == 3:
                    f = 0
                else:
                    f += 2
            else:
                if f == 0:
                    f = 2
                else:
                    f -= 2
        if card.action == 'reverse':
            increment *= -1

        if card.color == 'wild':
            color_swap()

        # handles both +4 and +2
        if card.action[0] == '+':
            times = int(card.action[1])
            for i in range(times):
                # next player.draw_card()
                pass

    poolCard = card 


def color_swap():
    pass

while True:
    socketio.on_event('play', process_move(data))
    # socketio.on_event('draw', player.draw_card())

    """
    if len(player.hand) == 0:
        print('game has ended')
        socketio.to(room).emit('end', player)
        break
    """

    # it is 4 players per room so this will do
    if f == 3 and increment == 1   :
        f = 0
    elif f == 0 and increment == -1:
        f = 3
    else:
        f += increment

if __name__ == "__main__":
    socketio.run(app, debug=True)
# deck
