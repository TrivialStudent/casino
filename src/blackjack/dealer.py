from deck import *
from player import *
from hand import *
class Dealer(Player):
    def __init__(self):
        super().__init__(name="Dealer", password=None)

    def deal(self, deck):
        return deck.draw()

    def play(self, deck):
        while self.cards.value() < 17:
            self.cards.add(deck.draw())
