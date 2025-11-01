from .card import Card


class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card: Card):
        self.cards.append(card)

    def value(self):
        total = sum(card.bj_value for card in self.cards)
        number_aces = sum(1 for card in self.cards if card.value == 1)
        while total > 21 and number_aces > 0:
            total -= 10
            number_aces -= 1
        return total


    def bust(self):
        return self.value() > 21
    def blackjack(self):
        return self.value() == 21 and len(self.cards) == 2

