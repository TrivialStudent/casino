from .card import *
import random

class Deck(object):
    def __init__(self):
        self.cards = []
        self.discarded = []

    def fill(self):
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        values = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        for suit in suits:
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









