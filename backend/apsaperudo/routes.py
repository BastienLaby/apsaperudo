from flask import render_template, request, redirect

from apsaperudo.application import app
from apsaperudo.api.game import get_games_ids
from apsaperudo.api.player import get_players_ids, get_player_game
from apsaperudo.database.models import clear_db


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/db")
def db():
    data = {
        "games": get_games_ids(),
        "players": [
            {
                "id": player,
                "game": get_player_game(player)
            } for player in get_players_ids()
        ]
    }
    return render_template("db.html", data=data)


@app.route("/clear")
def clear():
    clear_db()
    return redirect('/db')