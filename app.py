from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_cors import CORS
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
size = 4 # size of the room--> can make some function to change this for each room later 


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
    players=[] 
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
                players.append(people[0])
                if i == size:
                    send("game is starting :D", room=k)
                    move_to_in_game(k)
                    del ROOMS[k]
                    #gamestart stops the countdown 
                    emit('gamestart',room=k) 
                    start_game(k)
                    game(k,players)
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

def start_game(room): 
    #making the game text box 
    emit('game_display', room=room)


def game(room, players):

    # variables to iterate through turns
    f = 0
    increment = 1
    poolCard = next(Player.deck)
    players = [Player(p) for p in players]
    cPlayer = None
    pnum = 1

    # emit hands to players
    for i in players:
        #to mark player's numbers 
        socketio.emit('playernum', pnum, room=i.name)
        pnum += 1 
        # b.identity because we're using strings for the front end
        socketio.emit('hand', [b.identity for b in i.hand], room=i.name)
        

    # the front end  should handle which cards are playable
    # it will be created everytime the function is run but it is only run once per game so it shouldn't be too much of  a problem
    def process_move(card, hand):
        card = Card(card)
        global size
        nonlocal f; nonlocal increment
        nonlocal poolCard; nonlocal players
        nonlocal cPlayer
        hand.remove(card)
        poolCard = card

        if card.isAction:
            # handles both +4 and +2
            if card.action[0] == '+':
                times = int(card.action[1])
                for i in range(times):
                    players[f + increment].draw_card()
            
            # because draw skips as well
            if card.action == 'skip' or card.action[0] == '+':
                if increment == 1:
                    if f == size - 1:
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
                newColor = None
                while not (newColor in ['green', 'yellow', 'red', 'blue']):
                    socketio.emit('newColor', room=cPlayer.name)

                    # might not be the best way to do it but it works, opening in write mode creates a file
                    socketio.on_event('newColor', print(data, file=open('ha.txt', 'w')))
                    newColor = open('ha.txt', 'r').readline().strip()

                poolCard.color = newColor


    while True:
        # so front end can handle which cards are playable
        socketio.emit('pool', poolCard.identity, room=room)
        cPlayer = players[f]
        numCards = len(cPlayer.hand)
        # should work maybe
        socketio.emit('unlock', room=cPlayer.name)
        #to show which player's turn it is 
        socketio.emit('turn', f, room=room) 

        # data should be a string, check unoClasses > new_deck > normal_deck to see formatting
        socketio.on_event('play', process_move(data, cPlayer.hand))
        
        # draw twice then skip
        if numCards <= len(cPlayer.hand) + 2:
            socketio.on_event('draw', cPlayer.draw_card())
            socketio.emit('hand', [b.identity for b in cPlayer.hand], room=cPlayer.name)
        else:
            print('Can\'t draw anymore, skipped')
            socketio.emit('draw limit', room=cPlayer.name)

        
        if len(cPlayer.hand) == 0:
            print('game has ended')
            socketio.emit('end', room=room)
            break
        

        # it is 4 players per room so this will do
        socketio.emit('lock', room=cPlayer.name)
        if f == size - 1 and increment == 1:
            f = 0
        elif f == 0 and increment == -1:
            f = size - 1
        else:
            f += increment


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='127.0.0.1')
