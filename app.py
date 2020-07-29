"""
Here is where the web app will run
mingjie avialble after 6pm eastern
TODO: rooms, hook up uno logic to this, rooms
TODO: player class, non generator deck
"""
from flask import Flask, render_template, url_for, flash, redirect, request
from receiveData import JoinForm
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_cors import CORS
from receiveData import JoinForm
import time
from unoClasses import Player, Card

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = '975c9775521fd39cba0f67c131bdf4b7'
socketio = SocketIO(app)
# for now I am just making it four people per game
Q = []
ROOMS = dict()
inGame = dict()
size = 4 #size of the room--> can make some function to change this for each room later 


# ROOMS={"roomid":[[player1,F],[player2,F],[player3,F],[player4,F]]}
# inGame={playersid:roomid}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('otherindex.html')


@socketio.on('connect')
def on_create():
    # global Q
    send("searching for a room...")
    print('searching for room')
    Q.append(request.sid)
    print(Q)
    if len(Q) >= size:
        make_room()


# creates and confirms that players are connected to a room by sending out ready signal
def make_room():
    roomid = str(time.time())
    print(f"new room {roomid}")
    for i in range(size):
        player = Q.pop(0)
        join_room(roomid, player)
        ROOMS.setdefault(roomid,[])
        ROOMS[roomid].append([player,False])
        emit('join_room', {'user': player}, room=roomid)
        print(player + " has entered the room " + roomid)
        send("are you ready?", room=player)
    socketio.emit('ready', room=roomid)
    # start some sort of countdown-->countdown in html


# mega ack confirm user and/ or if all users in a room are ready then starts game
@socketio.on('ready')
def confirm_ready():
    print("received ready signal from "+ request.sid)
    #tells client their ready signal has been accounted for 
    send("ready has been noted! please wait for other players to confirm ready")
    val_list = list(ROOMS.values())
    key_list = list(ROOMS.keys())
    i = 0

    for val in val_list:
        for v in val:
            if v[0] == request.sid:
                v[1] = True
    for k in key_list:
        for people in (ROOMS.get(k)):
            if people[1]:
                i += 1
                if i == size:
                    send("game is starting :D", room=k)
                    move_to_in_game(k)
                    del ROOMS[k]
                    print(ROOMS)
                    print(inGame)
                    #gamestart stops the countdown 
                    emit("gamestart",room=k)
                    start_game(k)
                    print("game in " + k + " is starting")
        i = 0


@socketio.on('not_ready')
def back_to_queue():
    nrplayer = request.sid
    keys = list(ROOMS.keys())
    room = ""
    #find the room that failed to get 4 readys 
    for k in keys:
        players = ROOMS.get(k)
        for player in players:
            if player[0] == nrplayer:
                room = k
                break
        if room != "":
            break
    #for multiple not readys 
    if room == "": 
        return 

    emit('refresh',room=room)
    time.sleep(5)

    players = ROOMS.get(room)
    for player in players: 
        leave_room(room, player[0])
    del ROOMS[room]


# move ready confirmed users from ROOMS to inGame
def move_to_in_game(ri):  # room id
    players = ROOMS[ri]
    for player in players:
        inGame[player[0]] = ri
"""
def start_game(room): 
    #making the game text box 
    emit("game_display", "hi",room=room)
    
    values=list(inGame.values())
    for v in val: 
"""


# variables to iterate through turns
f = 0
increment = 1
poolCard = next(Player.deck)

# the front end 
def process_move(card, hand):
    global f; global increment; global poolCard

    hand.remove(card)

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
            # color_swap()
            pass

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
    # socketio.on_event('play', process_move(data, hand=player.hand))
    # socketio.on_event('draw', player.draw_card())

    
    # if len(player.hand) == 0:
    #     print('game has ended')
    #     socketio.to(room).emit('end', player)
    #     break
    

    # it is 4 players per room so this will do
    if f == 3 and increment == 1   :
        f = 0
    elif f == 0 and increment == -1:
        f = 3
    else:
        f += increment


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='127.0.0.1')
# deck
