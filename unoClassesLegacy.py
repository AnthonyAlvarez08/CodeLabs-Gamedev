"""
This is where all the classes for the game will be defined and also the deck because it is large
"""
from random import randint


class Card:

    def __init__(self, card_type, color, numAction):
        self.type = card_type  # either action or number
        self.color = color
        self.numAction = numAction  # like 6 or 9 or skip
        self.identity = f'{self.color} {self.numAction} {self.type}'

    # a string for now, should be a graphic picture
    def __repr__(self):
        return f'{self.color} {self.numAction} {self.type}'

# will generate a new random card
def new_card():
    colors = ["blue", "red", "orange", "purple", "pink", "yellow", "green"]
    numsActions = ['0', '1', '2', '3', '4',
                    '5', '6', '7', '8', '9',
                    'cancel', 'reverse', '+2',
                    '+4', 'change']

    cardNumAction = numsActions[randint(0, len(numsActions) - 1)]

    # if this action/ is in the last  b
    if cardNumAction in numsActions[13:]:
        cardColor = "change"
    else:
        cardColor = colors[randint(0, len(colors) - 1)]

    if cardNumAction in numsActions[10:]:
        cardType = "action"
    else:
        cardType = "number"

    return Card(cardType, cardColor, cardNumAction)


previousCard = new_card() 

class Player:

    # this is a constructor
    def __init__(self, name="Player"):
        self.name = name
        self.hand = list()  # or an array
        for i in range(6):
            self.draw_card()
        self.numCards = len(self.hand) # needs to be updated

    # draws a card, a function so it is easier
    def draw_card(self):
        self.hand.append(new_card())
        self.numCards = len(self.hand)

    def play_card(self, previousCard):
        index = int(input('what card to play (select number)?  '))

        acceptable = False

        try:
            assert self.numCards > index
        except AssertionError:
            print('You can\'t play that card')
            return 'unacceptable'
            
        if previousCard.color == self.hand[index].color:
            acceptable = True
        elif previousCard.numAction == self.hand[index].numAction:
            acceptable = True
        elif self.hand[index].color == 'change':
            acceptable = True

        if acceptable:
            card = self.hand.pop(index)
            self.numCards = len(self.hand)
            return card
        else:
            print('You can\'t play that card')
            return 'unacceptable'

    def show_hand(self):
        print(self.hand)

    def __repr__(self):
        return self.name

