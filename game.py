"""
Should we make our own custom cards?
If need be I can just make the game be a function
This is not finished yet
TODO: win condition, uno yelling, drawing when can't play, sometimes can't play cards with same number
"""

from unoClasses import new_card, Card, Player, previousCard

numPlayers = int(input('How many players in this session?  '))

players = [Player(f'Player {i + 1}') for i in range(numPlayers)]

# prompts for a color, checks if it is acceptable and then returns it
def color_change():
    try:
        newColor = str(input('What color would you like it to be?  '))
        assert newColor in ["blue", "red", "orange", "purple", "pink", "yellow", "green"]
    except:
        print('That\'s not a valid color')
        color_change()
    
    return newColor

# f keeps track of whose turn it is and increment makes the turn changes
f = 0
increment = 1
while True:
    print('\nOn top of the pile is a', previousCard)
    print(f'{players[f].name}\'s cards are:')
    for i, card in enumerate(players[f].hand):
        print(i, card)

    previousCard = players[f].play_card()

    if previousCard.color == 'change':
        previousCard.color = color_change()
    if previousCard.num_action == 'cancel':
        f += 2 * increment
        continue
    if previousCard.num_action == 'reverse':
        # basically a toggle
        increment *= -1
    
    # need to account for cycles
    if previousCard.num_action == '+2' or previousCard.num_action == '+4':
        _, change = map(str, list(previousCard.num_action))
        change = int(change)
        if increment == 1:
            if f < numPlayers - 1:
                for i in range(change): 
                    players[f + increment].draw_card()
            else:
                for i in range(change):
                    players[0].draw_card()
        else:
            if f == 0:
                for i in range(change):
                    players[numPlayers - 1].draw_card()
            else:
                for i in range(change):
                    players[f + increment].draw_card()


    f += increment

    # cycling management
    if f >= numPlayers - 1: f = 0
    if f <= 0: f += numPlayers - 1
