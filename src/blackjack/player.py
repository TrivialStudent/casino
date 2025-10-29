from .hand import Hand
import json
from pathlib import Path
import bcrypt
class Player:
    def __init__(self, name, password, balance=500,wins=0,losses=0, balance_history=None, total_winnings=0, total_losses=0, hashed=False):
        self.name = name
        self.pref_name = pref_name
        self.balance = balance
        self.cards = Hand()
        self.bet = 0
        self.wins = wins
        self.losses = losses
        self.total_winnings = total_winnings
        self.total_losses = total_losses
        self.balance_history = balance_history if balance_history else [balance]
        if password is None:
            self.password = None
        elif hashed:
            self.password = password.encode("utf-8")
        else:
            self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    def place_bet(self, amount):
        if amount > self.balance:
            raise ValueError("Amount can't be greater than balance")
        self.bet = amount
        self.balance -= amount
    def win(self):
        self.balance += self.bet * 2
        self.total_winnings += self.bet
        self.record_balance()
        self.wins += 1
    def tie(self):
        self.balance += self.bet
        self.record_balance()
        self.bet = 0
    def lose(self):
        self.total_losses += self.bet
        self.bet = 0
        self.record_balance()
        self.losses += 1
    def add_balance(self, amount):
        self.balance += amount
        self.record_balance()
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def win_ratio(self):
        total = self.wins + self.losses
        return float(self.wins) / total if total else 0.0
    def record_balance(self):
        self.balance_history.append(self.balance)

    def __str__(self):
        return f"name: {self.name}, balance: {self.balance}, wins: {self.wins}, losses: {self.losses}, password: {self.password}, total_winnings: {self.total_winnings}, total_losses: {self.total_losses}, total_winnings: {self.total_winnings}, total_losses: {self.total_losses}"


class Players:
    list_of_players = []
    file = Path("user_data.json")
    @classmethod
    def print_players(cls):
        for player in cls.list_of_players:
            print(player)
    @classmethod
    def add_player(cls, player):
        if any(p.name == player.name for p in cls.list_of_players):
            raise ValueError(f"A player with {player.name} already exists")
        cls.list_of_players.append(player)
        cls.save()
    @classmethod
    def save(cls):
        json_data = [{"name": p.name, "pref_name": p.pref_name, "password": p.password.decode("utf-8"), "balance": p.balance, "wins": p.wins, "losses": p.losses, "total_winnings": p.total_winnings, "total_losses": p.total_losses, "balance_history": p.balance_history} for p in cls.list_of_players]
        cls.file.write_text(json.dumps(json_data, indent=4))
    @classmethod
    def load(cls):
        if cls.file.exists():
            data = json.loads(cls.file.read_text())
            for p in data:
                player = Player(
                    p["name"],
                    p["pref_name"],
                    p["password"],
                    p["balance"],
                    p["wins"],
                    p["losses"],
                    p["balance_history"],
                    total_winnings=p.get("total_winnings", 0),
                    total_losses=p.get("total_losses", 0),
                 
                    hashed=True
                )
                cls.list_of_players.append(player)

    @classmethod
    def sign_in(cls, username):
        for player in cls.list_of_players:
            if username.strip() == player.name.strip():
                while True:
                    password = input("Enter password, or enter nothing to go back: ").strip()
                    if player.verify_password(password):
                        print(f"Welcome back {player.pref_name}")
                        return player
                    elif password == "":
                        break
                    else:
                        print("Wrong password")
        print(f"No player named {username}")
        return None





