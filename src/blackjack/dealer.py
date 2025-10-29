
from .player import *

class Dealer(Player):
    def __init__(self):
        super().__init__(name="Dealer", password=None, pref_name="BOB")

    def deal(self, deck):
        return deck.draw()

    def play(self, deck):
        while self.cards.value() < 17:
            self.cards.add(deck.draw())
