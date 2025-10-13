from hand import *

class Player:
    def __init__(self, name, password):
        self.name = name
        self.balance = 0
        self.cards = Hand()
        self.bet = 0
        self.wins = 0
        self.losses = 0
        self.password = password
    def place_bet(self, amount):
        if amount > self.balance:
            raise ValueError("Amount can't be greater than balance")
        self.bet = amount
        self.balance -= amount
    def win(self):
        self.balance += self.bet * 2
        self.wins += 1
    def tie(self):
        self.balance += self.bet
        self.bet = 0
    def lose(self):
        self.bet = 0
        self.losses += 1
    def add_balance(self, amount):
        self.balance += amount
