from flask import render_template, request, redirect

from apsaperudo.application import app
from apsaperudo.api.game import get_games_names
from apsaperudo.api.lobby import get_pending_players_ids, get_pending_players_names, get_pending_players_games
from apsaperudo.database.models import clear_db


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/db")
def db():
    players_names = get_pending_players_names()
    players_ids = get_pending_players_ids()
    players_games = get_pending_players_games()
    assert len(players_names) == len(players_ids) == len(players_games)

    data = {
        "games": get_games_names(),
        "players": [
            {
                "name": players_names[i],
                "id": players_ids[i],
                "game": players_games[i]
            } for i in range(len(players_names))
        ]
    }
    return render_template("db.html", data=data)


@app.route("/clear")
def clear():
    clear_db()
    return redirect('/db')