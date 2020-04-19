from flask import render_template, request

from apsaperudo.application import app
from apsaperudo.api.game import get_games
from apsaperudo.api.lobby import get_pending_players_ids, get_pending_players_names


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/db")
def db():
    players_names = get_pending_players_names()
    players_ids = get_pending_players_ids()
    assert len(players_names) == len(players_ids)

    data = {
        "games": get_games(),
        "players": [
            {
                "name": players_names[i],
                "id": players_ids[i]
            } for i in range(len(players_names))
        ]
    }
    return render_template("db.html", data=data)
