"""
Should we make our own custom cards?
If need be I can just make the game be a function
This is not finished yet
TODO: uno yelling, drawing when can't play, add the rules
"""

from unoClasses import new_card, Card, Player, previousCard

numPlayers = int(input('How many players in this session?  '))

players = [Player(f'Player {i + 1}') for i in range(numPlayers)]

rules = input("Would you like to read the rules (y/n)?  ")
if rules == 'y' or rules == 'yes':
    print('''[insert rules]''')

# prompts for a color, checks if it is acceptable and then returns it
def color_change():
    newColor = str(input('What color would you like it to be?  '))
    if newColor in ["blue", "red", "orange", "purple", "pink", "yellow", "green"]:
        return newColor
    else:
        print('That\'s not a valid color')
        return color_change()
    

# prompt to draw card and try to play or skip turn
def unplayable(hand, topCard):
    for i in hand:
        if topCard.color == i.color:
            return False
        elif topCard.numAction == i.numAction:
            return False
        elif i.color == 'change':
            return False
    return True
    

# no start with action card
while previousCard.type == 'action':
    previousCard = new_card()

# f keeps track of whose turn it is and increment makes the turn changes
f = 0
increment = 1
while True:
    print('\nOn top of the pile is a', previousCard)
    print(f'{players[f].name}\'s cards are:')
    for i, card in enumerate(players[f].hand):
        print(i, card)
    
    # maybe works
    # draw if can't play
    while unplayable(players[f].hand, previousCard):
        print('you have no cards that can be played!')
        choice = input('would you like to skip your turn or draw a card? (skip/draw)  ')
        if choice == 'skip' or choice == 's':
            f += increment
            continue
        elif choice == 'draw' or choice == 'd':
            # need to print hand again
            players[f].draw_card()
            print(f'New card is {players[f].hand(players[f].numCards - 1)}')


            

    temp = previousCard
    previousCard = players[f].play_card(previousCard=temp)
    while previousCard == 'unacceptable':
        previousCard = players[f].play_card(previousCard=temp)

    if players[f].numCards == 0:
        print(f'{players[f].name} won!\n\nThank you so much for playing my game!')
        break

    if previousCard.color == 'change':
        previousCard.color = color_change()
        
    # maybe works
    if previousCard.numAction == 'cancel':
        if f == numPlayers - 2:
            f = 0
        elif f == 0:
            f = numPlayers - 1
        else:
            f += 2 * increment
        print('\nNext player has been skipped!')
        continue

    if previousCard.numAction == 'reverse':
        # basically a toggle
        print('\nCycle Reversed')
        increment *= -1
    
    # need to account for cycles
    if previousCard.numAction == '+2' or previousCard.numAction == '+4':
        _, change = map(str, list(previousCard.numAction))
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
    if f > numPlayers - 1:
         f = 0
    elif f < 0:
         f += numPlayers
    
