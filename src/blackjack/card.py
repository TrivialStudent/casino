
class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def __str__(self):
        self.name= ""
        if self.value == 11:
            self.name = "Jack"
        elif self.value == 12:
            self.name = "Queen"
        elif self.value == 13:
            self.name = "King"
        elif self.value == 1:
            self.name = "Ace"
        else:
            self.name = self.value


        return f'{self.name} of {self.suit}'


    def get_blackjack_value(self):
        if self.value == 1:
            return 11
        elif self.value >= 10:
            return 10
        return self.value