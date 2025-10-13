
from dealer import *
from deck import *
from player import *
import time
class Blackjack():
    def __init__(self, player: Player):
        self.player_account = player
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()
        self.dealer = Dealer()

    def start(self):
        self.player_account.cards = Hand()
        self.dealer.cards = Hand()
        while True:
            try:
                print(
                    f"How much would you like to bet? [{self.player_account.name}'s balance is {self.player_account.balance}]")
                amount = int(input("Amount: "))
                if amount < 1:
                    print("Minimum bet is 1.")
                    continue
                self.player_account.place_bet(amount)
                break
            except ValueError as e:
                print(e)
            except Exception:
                print("Please enter a valid integer.")

    def deal_cards(self):
        for _ in range(2):
            self.player_account.cards.add(self.deck.draw())
            self.dealer.cards.add(self.deck.draw())
    def show(self):
        time.sleep(1)
        print(f"Dealer cards: [REDACTED], {self.dealer.cards.cards[1]}")
        time.sleep(0.5)
        print("Dealing", end="")
        for _ in range(4):
            print(".", end="")
            time.sleep(0.3)
        print()
        print(f"Player cards: {[str(card) for card in self.player_account.cards.cards]}, total value: {self.player_account.cards.value()}")
    def player_turn(self):
        while True:
            self.show()
            time.sleep(1)
            if self.player_account.cards.bust():
                print("Game over")
                print( f"Losings: {self.player_account.balance + self.player_account.bet} -= {self.player_account.bet} = {self.player_account.balance }")

                self.player_account.lose()
                return False
            print()
            while True:
                print("hit or stand? ")
                turn = input("DECISION: ")
                if turn == "hit":
                    self.player_account.cards.add(self.deck.draw())
                    break
                elif turn == "stand":
                    return True
                else:
                    print("Enter hit or stand")
                    continue
    def dealer_turn(self):
        print("Revealing dealer's hand", end="")
        for _ in range(4):
            print(".", end="")
            time.sleep(0.3)
        print()
        self.dealer.play(self.deck)
        print(f"Dealer cards: {[str(card) for card in self.dealer.cards.cards]}, total value: {self.dealer.cards.value()}")

    def resolve_round(self):
        temp_balance = self.player_account.balance
        player_val = self.player_account.cards.value()
        dealer_val = self.dealer.cards.value()
        print("Calculating", end="")
        for _ in range(4):
            print(".", end="")
            time.sleep(0.3)
        print()
        if self.player_account.cards.bust():
            print("Player busts. Dealer wins!")
            print(f"Losings: {self.player_account.balance + self.player_account.bet} -= {self.player_account.bet} = {self.player_account.balance}")
            self.player_account.lose()

        elif self.dealer.cards.bust() or player_val > dealer_val:
            print("Player wins!")
            self.player_account.win()
            print(f"Winnings: {temp_balance} += {self.player_account.bet} * 2 = {self.player_account.balance}")
        elif player_val == dealer_val:
            print("Push (tie).")
            self.player_account.tie()
            print(f"Balance = {self.player_account.balance}")
        else:
            print("Dealer wins!")
            print(f"Losings: {self.player_account.balance + self.player_account.bet} -= {self.player_account.bet} = {self.player_account.balance}")
            self.player_account.lose()


if __name__ == "__main__":
    trashbot = Player("lorcan", "1234")
    trashbot.add_balance(1000)
    game = Blackjack(trashbot)
    while True:
        game.start()
        game.deal_cards()
        if not game.player_turn():
            again = input("\nYou busted! Play again? (y/n): ").lower()
            if again != "y":
                break
            else:
                continue
        game.dealer_turn()
        game.resolve_round()
        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            break





