"""
Should we make our own custom cards?
If need be I can just make the game be a function
This is not finished yet
"""

from unoClasses import new_card, Card, Player, previousCard

num_players = int(input('How many players in this session?  '))

players = [Player(f'Player {i + 1}') for i in range(num_players)]

def colorChange():
    try:
        newColor = str(input('What color would you like it to be?  '))
        assert newColor in ["blue", "red", "orange", "purple", "pink", "yellow", "green"]
    except:
        print('That\'s not a valid color')
        colorChange()
    finally:
        return newColor

# we might need to change this into javascript so I'll keep it as simple as possible
f = 0
increment = 1
while True:
    print('\nOn top of pile is', previousCard)
    print('Your cards are:')
    for i, card in enumerate(players[f].hand):
        print(i, card)

    previousCard = players[f].play_card()

    if previousCard.color == 'change':
        previousCard.color = colorChange()
    elif previousCard.num_action == 'cancel':
        f += 2 * increment
        continue
    elif previousCard.num_action == 'reverse':
        # basically a toggle
        increment *= -1
    elif previousCard.num_action == '+2':
        for i in range(2): players[f + increment].draw_card()
    elif previousCard.num_action == '+4':
        for i in range(4): players[f + increment].draw_card()


    f += increment
