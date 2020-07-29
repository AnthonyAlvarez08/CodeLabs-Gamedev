from random import shuffle

class Card:

    def __init__(self, string):
        isAction, num, color, *action = string.split()
        self.identity = string
        self.isAction = bool(int(isAction))
        self.num = int(num)
        self.color = str(color)
        if self.isAction:
            self.action = action[0]

    def __repr__(self):
        if self.isAction:
            return f'action {self.action} {self.color}'
        return f'number {self.num} {self.color}'



"""
The deck consists of 108 cards: four each of "Wild" and "Wild Draw Four,"
and 25 each of four different colors (red, yellow, green, blue).
Each color consists of one zero, two each of 1 through 9, 
and two each of "Skip," "Draw Two," and "Reverse." 
These last three types are known as "action cards."
"""


def new_deck():
    # standard uno deck
    normal_deck = [
        "0 0 red", "0 1 red", "0 1 red", "0 2 red", "0 2 red", "0 3 red",
        "0 3 red", "0 4 red", "0 4 red", "0 5 red", "0 5 red", "0 6 red",
        "0 6 red", "0 7 red", "0 7 red", "0 8 red", "0 8 red", "0 9 red",
        "0 9 red", "1 -1 red skip", "1 -1 red skip", "1 -1 red +2",
        "1 -1 red +2", "1 -1 red reverse", "1 -1 red reverse",
        "0 0 yellow ", "0 1 yellow", "0 1 yellow", "0 2 yellow", "0 2 yellow",
        "0 3 yellow", "0 3 yellow", "0 4 yellow", "0 4 yellow", "0 5 yellow",
        "0 5 yellow", "0 6 yellow", "0 6 yellow", "0 7 yellow", "0 7 yellow",
        "0 8 yellow", "0 8 yellow", "0 9 yellow", "0 9 yellow",
        "1 -1 yellow skip", "1 -1 yellow skip", "1 -1 yellow +2",
        "1 -1 yellow +2", "1 -1 yellow reverse", "1 -1 yellow reverse",
        "0 0 green", "0 1 green", "0 1 green", "0 2 green", "0 2 green", "0 3 green",
        "0 3 green", "0 4 green", "0 4 green", "0 5 green", "0 5 green", "0 6 green",
        "0 6 green", "0 7 green", "0 7 green", "0 8 green", "0 8 green", "0 9 green",
        "0 9 green", "1 -1 green skip", "1 -1 green skip", "1 -1 green +2", "1 -1 green +2",
        "1 -1 green reverse", "1 -1 green reverse", "0 0 blue", "0 1 blue", "0 1 blue",
        "0 2 blue", "0 2 blue", "0 3 blue", "0 3 blue", "0 4 blue", "0 4 blue",
        "0 5 blue", "0 5 blue", "0 6 blue", "0 6 blue", "0 7 blue", "0 7 blue",
        "0 8 blue", "0 8 blue", "0 9 blue", "0 9 blue", "1 -1 blue skip",
        "1 -1 blue skip", "1 -1 blue +2", "1 -1 blue +2", "1 -1 blue reverse",
        "1 -1 blue reverse", "1 -1 wild +4", "1 -1 wild +4", "1 -1 wild +4",
        "1 -1 wild +4", "1 -1 wild wild", "1 -1 wild wild", "1 -1 wild wild",
        "1 -1 wild wild"
    ]
    shuffle(normal_deck)
    return map(Card, normal_deck)


class Player:

    # new_deck returns a map object which is exhaustable, needs to be refreshed
    deck = new_deck()

    def __init__(self, name):
        self.name = name
        self.hand = list()
        for i in range(7):
            self.draw_card()
        print(f'Welcome {name}!')

    @classmethod
    def refresh_deck(cls):
        cls.deck = new_deck()
        print('deck reshuffled!')

    # the front end will handle valid moves
    def handle_move(self):
        pass

    def draw_card(self):
        print('time to draw!')
        try:
            self.hand.append(next(Player.deck))
        except StopIteration:
            Player.refresh_deck()
            self.hand.append(next(Player.deck))
            
