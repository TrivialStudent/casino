
class Card:
    SUIT_SYMBOLS = {"Spades":"♠", "Hearts":"♥", "Diamonds":"♦", "Clubs":"♣"}

    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    @property
    def rank_short(self):
        return {1:"A", 11:"J", 12:"Q", 13:"K"}.get(self.value, str(self.value))

    @property
    def suit_symbol(self):
        return self.SUIT_SYMBOLS.get(self.suit, self.suit)

    @property
    def bj_value(self):
        if self.value == 1:
            return 11
        if self.value >= 10:
            return 10
        return self.value

    def __str__(self):
        return f'{self.rank_short}{self.suit_symbol}'