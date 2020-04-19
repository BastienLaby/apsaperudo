from flask import request
from flask_socketio import join_room, leave_room, rooms, emit, send

from apsaperudo.application import app
from apsaperudo.io.messages import message_to_player, message_to_game

socketio = app.extensions["socketio"]


@socketio.on("connect", namespace="/apsaperudo")
def connect_handler():
    """
    Connection should be made when the client enters the front page.
    """
    print("Connected")
    message_to_player("connection_ok", {
        "message": "Connected !",
        "username": "Michel"
    })
    message_to_player("games_updated", {
        "message": "Games list updated.",
        "games": ["game01", "game02"]
    })


@socketio.on("disconnect", namespace="/apsaperudo")
def disconnect_handler():
    """
    Received when the socket is removed or if the client closes the tab.
    """
    # TODO: remove the client from game and game room
    pass


@socketio.on("create_game", namespace="/apsaperudo")
def on_game_create(data):
    """
    Create a new game with the given name (duplicates names are allowed for now).
    Create a new player for the game creator.
    """
    # TODO: create game
    on_game_join(data)


@socketio.on("join_game", namespace="/apsaperudo")
def on_game_join(data):
    assert all(i in data for i in ("game_id", "username"))
    for room in rooms()[1:]:
        on_game_leave({"game_id": room, "username": data["username"]})
    message_to_player("game_joined", {
        "message": f'You entered #{data["game_id"]}',
        "game_id": data["game_id"]
    })
    message_to_game(
        "player_joined", {
            "message": f'#{data["username"]} entered the game'
        },
        data["game_id"]
    )
    join_room(data["game_id"])


@socketio.on("leave_game", namespace="/apsaperudo")
def on_game_leave(data):
    assert all(i in data for i in ("game_id", "username"))
    leave_room(data["game_id"])
    message_to_player("game_leaved", {
        "message": f'You left #{data["game_id"]}',
        "game_id": data["game_id"]
    })
    message_to_game(
        "player_leaved", {
            "message": f'#{data["username"]} left the game'
        },
        data["game_id"]
    )


@socketio.on("start_game", namespace="/apsaperudo")
def on_game_start(data):
    """
    Start the game with the current registered players.
    """
    message_to_game(666, "game_started", {"message": "Game has started !"})
