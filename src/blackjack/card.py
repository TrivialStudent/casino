
class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f'{self.value} of {self.suit}'


    def get_blackjack_value(self):
        if self.value == 1:
            return 11
        elif self.value >= 10:
            return 10
        return self.value