from deck import *

class Dealer:
    def __init__(self):
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()

    def deal(self):
        return self.deck.draw()
