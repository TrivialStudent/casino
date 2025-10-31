import json

from flask import Flask, render_template, request, redirect, url_for, session, flash
from blackjack.deck import Deck
from blackjack.hand import Hand
from blackjack.dealer import Dealer
from blackjack.player import Player, Players

import bcrypt

import os
import pathlib
import subprocess, sys

BASE_DIR = pathlib.Path(__file__).resolve().parent
PLINKO_DIR = (BASE_DIR / "plinko").resolve()     # e.g. C:\...\casino2\src\plinko
PLINKO_MAIN = (PLINKO_DIR / "main.py").resolve()


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
            "round_active": False,  # no bet yet
            "log": []
        }
        g = GAMES[user.name]
        g["deck"].fill()
        g["deck"].shuffle()
    return GAMES[user.name]

def log(g, *lines):
    g["log"].extend(lines)

def render_hidden_dealer(dealer: Dealer):
    if len(dealer.cards.cards) >= 2:
        vis = dealer.cards.cards[1]
        return (
            f"Dealer cards: [Hidden], {vis}",
            f"Dealer total value: ? + {vis.get_blackjack_value()}"
        )
    elif len(dealer.cards.cards) == 1:
        return ("Dealer cards: [Hidden]", "Dealer total value: ?")
    else:
        return ("Dealer has no cards yet.", "")

def render_full_dealer(dealer: Dealer):
    cards_text = ", ".join(str(c) for c in dealer.cards.cards)
    return f"Dealer cards: [{cards_text}], total value: {dealer.cards.value()}"

def render_player(user: Player):
    cards_text = ", ".join(str(c) for c in user.cards.cards)
    return f"Player cards: [{cards_text}], total value: {user.cards.value()}"

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

@app.route("/plinko", methods=["GET"])
def plinko_page():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    # Minimal inline HTML to avoid creating a new template file
    return f"""
    <!doctype html>
    <html><head><meta charset="utf-8"><title>Plinko</title></head>
    <body style="font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin:2rem;">
      <h1>Plinko</h1>
      <p>Logged in as: <strong>{user.name}</strong></p>
      <form method="post" action="{url_for('plinko_run')}">
        <button type="submit" style="padding:.6rem 1rem; font-size:1rem;">Play Plinko</button>
      </form>
      <p style="margin-top:1rem; color:#666;">
        A game window will open on the machine running this Flask app. Closing the window or pressing Q will save your balance to <code>user_data.json</code>.
      </p>
    </body></html>
    """

@app.route("/plinko/run", methods=["POST", "GET"])
def plinko_run():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    env = os.environ.copy()
    env["PLINKO_USER"] = user.name

    if sys.platform.startswith("win"):
        DETACHED = 0x00000008  # DETACHED_PROCESS
        subprocess.Popen(
            [sys.executable, str(PLINKO_MAIN)],
            env=env,
            creationflags=DETACHED,
            close_fds=True
        )
    else:
        subprocess.Popen(
            [sys.executable, str(PLINKO_MAIN)],
            env=env,
            start_new_session=True,
            close_fds=True
        )

    return ("", 204)


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
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))

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
        log="\n".join(g["log"]),
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
        g["log"].clear()


        h1, h2 = render_hidden_dealer(g["dealer"])
        log(g,
            f"Bet: {amount}. Balance now: {user.balance}",
            h1, h2,
            render_player(user)
        )
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
    log(g, "Player hits.", render_player(user))

    if user.cards.bust():
        log(g, "Player busts! Round over.")
        # lose() assumes bet already deducted
        user.lose()
        g["round_active"] = False
        Players.save()
    else:
        # re-log dealer hidden state
        h1, h2 = render_hidden_dealer(g["dealer"])
        log(g, h1, h2)

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

    log(g, "Player stands.", "Revealing dealer hand...")

    # reveal dealer, then have dealer play
    log(g, render_full_dealer(g["dealer"]))
    g["dealer"].play(g["deck"])   # dealer hits to 17+
    log(g, "Dealer final:", render_full_dealer(g["dealer"]))

    # resolve
    p_val = user.cards.value()
    d_val = g["dealer"].cards.value()

    if user.cards.bust():
        log(g, f"Player busts. Dealer wins. (p={p_val}, d={d_val})")
        user.lose()
    elif g["dealer"].cards.bust() or p_val > d_val:
        old = user.balance
        user.win()
        log(g, f"Player wins! Balance: {old} + bet*2 = {user.balance} (p={p_val}, d={d_val})")
    elif p_val == d_val:
        old = user.balance
        user.tie()
        log(g, f"Push. Balance: {old} + bet = {user.balance} (p={p_val}, d={d_val})")
    else:
        log(g, f"Dealer wins. (p={p_val}, d={d_val})")
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