from ..blackjack.player import *


def welcome():
    print(f"Welcome to Santos Casino! Would you like to sign in, or create a new account?")
    while True:
        choice = input("Sign in (S) / Create new (C): ")
        if choice == "S":
            pass
        elif choice == "C":
            print(f"Great, enter a unique username")
            name = input("Username: ")
            Players.add_player(name)
        else:
            print("Invalid choice. Please try again.")


def sign_in():
    print("Please enter username: ")