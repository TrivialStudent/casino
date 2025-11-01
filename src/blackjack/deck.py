from .card import *
import random

class Deck(object):
    def __init__(self):
        self.cards = []
        self.discarded = []

    def fill(self):
        self.cards.clear()
        SUITS = ["♠", "♥", "♦", "♣"]
        values = range(1, 14)
        for suit in SUITS:
            for value in values:
                self.cards.append(Card(value, suit))
    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            self.cards, self.discarded = self.discarded, []
            self.shuffle()
        return self.cards.pop()

    def discard(self, card):
        self.discarded.append(card)









