import json

from flask import Flask, render_template, request, redirect, url_for, session, flash
from blackjack.deck import Deck
from blackjack.hand import Hand
from blackjack.dealer import Dealer
from blackjack.player import Player, Players

import bcrypt

import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

app.secret_key = "dev-secret"  # replace in production

app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 600 #10 minutes

Players.load()


GAMES = {}

# ----------- helpers -----------

def current_user():
    name = session.get("user")
    if not name:
        return None
    for p in Players.list_of_players:
        if p.name == name:
            return p
    return None

def ensure_game(user: Player):
    if user.name not in GAMES:
        GAMES[user.name] = {
            "deck": Deck(),
            "dealer": Dealer(),
            "round_active": False,
        }
        g = GAMES[user.name]
        g["deck"].fill()
        g["deck"].shuffle()
    return GAMES[user.name]

def render_hidden_dealer(dealer: Dealer):
    if len(dealer.cards.cards) >= 2:
        vis = dealer.cards.cards[1]
        return (
            f"Dealer cards: ?, {vis}",
            f"Dealer total value: ? + {vis.bj_value}"
        )
    elif len(dealer.cards.cards) == 1:
        return ("Dealer cards: ?", "Dealer total value: ?")
    else:
        return ("Dealer has no cards yet.", "")

def render_full_dealer(dealer: Dealer):
    cards_text = ", ".join(str(c) for c in dealer.cards.cards)
    return f"Dealer cards: [{cards_text}]"

def render_player(user: Player):
    cards_text = ", ".join(str(c) for c in user.cards.cards)
    return f"Player cards: [{cards_text}]"

# ------------- Routes ---------------
@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/stats")
def stats():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    win_ratio = round(user.win_ratio() * 100, 2)
    net_earnings = user.total_winnings - user.total_losses
    return render_template(
        "stats.html",
        user=user,
        pref_name = user.pref_name,
        win_ratio=win_ratio,
        total_winnings=user.total_winnings,
        losses=user.total_losses,
        net_earnings=net_earnings,
        balance_history=json.dumps(user.balance_history)
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        pref_name = request.form["pref_name"].strip()
        if not username or not password:
            flash("Username and password required.", "error")
            return redirect(url_for("signup"))
        if any(p.name == username for p in Players.list_of_players):
            flash("Username already exists.", "error")
            return redirect(url_for("signup"))


        player = Player(username, pref_name, password)
        Players.add_player(player)
        session["user"] = player.name
        flash("Account created succesfully!", "success")
        return redirect(url_for("home"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # Find user
        player = next((p for p in Players.list_of_players if p.name == username), None)
        if not player:
            flash("User does not exist.", "error")
            return redirect(url_for("login"))

        # Verify
        if bcrypt.checkpw(password.encode("utf-8"), player.password):
            session["user"] = player.name
            flash(f"Welcome, {player.pref_name}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Wrong password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out.", "success")
    return redirect(url_for("login"))

@app.route("/home")
def home():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("index.html", user=user)

@app.route("/play", methods=["GET"])
def play():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    g = ensure_game(user)

    return render_template(
        "game.html",
        user=user,
        dealer_cards=g["dealer"].cards.cards,
        player_cards=user.cards.cards,
        player_total=user.cards.value(),
        dealer_total=g["dealer"].cards.value(),
        round_active=g["round_active"]
    )

@app.route("/bet", methods=["POST"])
def bet():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    g = ensure_game(user)
    if g["round_active"]:
        flash("Round already in progress.", "info")
        return redirect(url_for("play"))

    try:
        amount = int(request.form["amount"])
        if amount < 1:
            flash("Minimum bet is 1.", "error")
            return redirect(url_for("play"))
        # start a round (no input/print; call backend)
        user.cards = Hand()
        g["dealer"].cards = Hand()
        user.place_bet(amount)
        # initial deal
        for _ in range(2):
            user.cards.add(g["deck"].draw())
            g["dealer"].cards.add(g["deck"].draw())
        g["round_active"] = True

        h1, h2 = render_hidden_dealer(g["dealer"])

        flash(f"Current bet: ${amount}", "info")
    except ValueError:
        flash("Enter a valid integer bet.", "error")

    return redirect(url_for("play"))

@app.route("/hit", methods=["POST"])
def hit():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    g = ensure_game(user)
    if not g["round_active"]:
        flash("No active round. Place a bet.", "info")
        return redirect(url_for("play"))

    user.cards.add(g["deck"].draw())
    flash("Player hits.", "info")

    if user.cards.bust():
        # lose() assumes bet already deducted
        user.lose()
        g["round_active"] = False
        Players.save()
        flash("Bust! Dealer wins.", "error")
    else:
        # re-log dealer hidden state
        h1, h2 = render_hidden_dealer(g["dealer"])

    return redirect(url_for("play"))

@app.route("/stand", methods=["POST"])
def stand():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    g = ensure_game(user)
    if not g["round_active"]:
        flash("No active round. Place a bet.", "info")
        return redirect(url_for("play"))

    flash("Player stands. Revealing dealer hand...", "info")

    # reveal dealer, then have dealer play
    g["dealer"].play(g["deck"])   # dealer hits to 17+

    # resolve
    p_val = user.cards.value()
    d_val = g["dealer"].cards.value()

    if user.cards.bust():
        flash("Bust! Dealer wins.", "error")
        user.lose()
    elif g["dealer"].cards.bust() or p_val > d_val:
        old = user.balance
        user.win()
        flash("Player wins!", "success")
    elif p_val == d_val:
        old = user.balance
        user.tie()
        flash("Push.", "info")
    else:
        flash("Dealer wins.", "error")
        user.lose()

    g["round_active"] = False
    Players.save()
    return redirect(url_for("play"))

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            amount = int(request.form["amount"])
            if amount <= 0 or amount > 9999999:
                flash("Deposit must be greater than 0, and you can't deposit more than 9999999. Try again", "error")
            else:
                user.balance += amount
                Players.save()
                return redirect(url_for("home"))
        except ValueError:
            flash("Please enter a valid number", "error")
            return redirect(url_for("deposit"))
    return render_template("deposit.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)