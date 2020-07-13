"""
This is where all the classes for the game will be defined and also the deck because it is large
"""
from random import randint


class Card:

    def __init__(self, card_type, color, num_action):
        self.type = card_type  # either action or number
        self.color = color
        self.num_action = num_action  # like 6 or 9 or skip
        self.identity = f'{self.color} {self.num_action} {self.type}'

    # a string for now, should be a graphic picture
    def __repr__(self):
        return f'{self.color} {self.num_action} {self.type}'

# will generate a new random card
def new_card():
    colors = ["blue", "red", "orange", "purple", "pink", "yellow", "green"]
    nums_actions = ['0', '1', '2', '3', '4',
                    '5', '6', '7', '8', '9',
                    'cancel', 'reverse', '+2',
                    '+4', 'change']

    card_num_action = nums_actions[randint(0, len(nums_actions) - 1)]

    # if this action/ is in the last  b
    if card_num_action in nums_actions[13:]:
        card_color = "change"
    else:
        card_color = colors[randint(0, len(colors) - 1)]

    if card_num_action in nums_actions[10:]:
        card_type = "action"
    else:
        card_type = "number"

    return Card(card_type, card_color, card_num_action)


previousCard = new_card() 

class Player:

    # this is a constructor
    def __init__(self, name="Player"):
        self.name = name
        self.hand = list()  # or an array
        for i in range(10):
            self.draw_card()
        self.num_cards = len(self.hand) # needs to be updated

    # draws a card, a function so it is easier
    def draw_card(self):
        self.hand.append(new_card())
        self.num_cards = len(self.hand)

    def play_card(self):
        global previousCard
        index = int(input('what card to play (select number)?  '))
        try:
            assert len(self.hand) > index
            if (previousCard.color == self.hand[index].color
                or previousCard.num_action == self.hand[index].num_action
                or self.hand[index].color == 'change') == False:
                raise ValueError
        except Exception as e:
            print("You can't play that card because", e)
            self.play_card()

        card = self.hand.pop(index)
        self.num_cards = len(self.hand)
        return card

    def show_hand(self):
        print(self.hand)

    def __repr__(self):
        return self.name

