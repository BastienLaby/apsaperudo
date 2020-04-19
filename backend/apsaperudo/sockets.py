from flask import request
from flask_socketio import join_room, leave_room, rooms
from faker import Faker

from apsaperudo.application import app
from apsaperudo.api.lobby import (
    create_pending_player,
    get_pending_players_names,
    rename_pending_player,
    delete_pending_player,
    create_pending_game,
    delete_pending_game
)
from apsaperudo.api.game import add_player_to_game, remove_player_from_game, get_games_names
from apsaperudo.io.messages import (
    message_to_player, message_to_game, message_to_all
)


socketio = app.extensions["socketio"]
_NAMESPACE = "/apsaperudo"


class PseudoGenerationAttemptsExceeded(Exception):
    pass


@socketio.on("connect", namespace=_NAMESPACE)
def connect_handler():
    """
    Connection should be made when the client enters the front page.
    """

    fake = Faker()
    attempts = 1000
    existing_players = get_pending_players_names()
    for i in range(attempts):
        username = fake.name()
        if username not in existing_players:
            break
    else:
        raise PseudoGenerationAttemptsExceeded()

    create_pending_player(request.sid, username)

    message_to_player("connection_ok", {
        "message": "Connected !",
        "username": username
    })
    message_to_player("games_updated", {
        "message": "Games list updated.",
        "games": get_games_names()
    })


@socketio.on("disconnect", namespace=_NAMESPACE)
def disconnect_handler():
    """
    Received when the socket is removed or if the client closes the tab.
    """
    # TODO: remove the client from game and game room

    user_rooms = rooms()
    username = delete_pending_player(request.sid)
    for room in user_rooms:
        message_to_game("player_leaved", {
                "message": f"#{username} left the game"
            }, room
        )


@socketio.on("change_username", namespace=_NAMESPACE)
def on_username_change(data):
    """
    Check if a pending player with the same name already exists.
    Return a "already_taken_username" event if so.
    Else, rename the player and return a "username_changed" event.
    """
    assert "new_username" in data
    new_username = data["new_username"]
    if new_username in get_pending_players_names():
        message_to_player("already_taken_username", {
            "message": f"Username \"{new_username}\" already taken."
        })
    else:
        rename_pending_player(request.sid, new_username)
        message_to_player("username_changed", {
            "message": f"Username changed to #{new_username}.",
            "username": new_username
        })


@socketio.on("create_game", namespace=_NAMESPACE)
def on_game_create(data):
    """
    Create a new game with the given name.
    If a game with the same name (pending or not) already exists, return a "already_taken_gamename" event.
    Else, create the game, return a "game_created" event, and make the player join it.
    """
    assert all(i in data for i in ("game_name", "username"))
    game_name = data["game_name"]
    if game_name in get_games_names():
        message_to_player("already_taken_gamename", {
            "message": f"Game name \"{game_name}\" already taken."
        })
    else:
        create_pending_game(game_name)
        message_to_player("game_created", {
            "message": f"Game #{game_name} created."
        })
        message_to_all("games_updated", {
            "message": "Games list updated.",
            "games": get_games_names()
        })
        on_game_join(data)


@socketio.on("join_game", namespace=_NAMESPACE)
def on_game_join(data):
    assert all(i in data for i in ("game_name", "username"))
    username = data["username"]
    game_name = data["game_name"]

    # disconnect from every rooms
    for room in rooms()[1:]:
        on_game_leave({"game_name": room, "username": username})

    # join the new game
    message_to_player("game_joined", {
        "message": f"You entered #{game_name}.",
        "game_name": game_name
    })
    message_to_game("player_joined", {
            "message": f"#{username} entered the game."
        }, game_name
    )
    join_room(game_name)
    add_player_to_game(game_name, request.sid)


@socketio.on("leave_game", namespace=_NAMESPACE)
def on_game_leave(data):
    """
    Leave the given game.
    If the game is empty, delete it.
    """
    assert all(i in data for i in ("game_name", "username"))
    username = data["username"]
    game_name = data["game_name"]


    leave_room(game_name)
    message_to_player("game_leaved", {
        "message": f"You left #{game_name}",
        "game_name": game_name
    })
    message_to_game("player_leaved", {
            "message": f"#{username} left the game"
        }, data["game_name"]
    )


@socketio.on("start_game", namespace=_NAMESPACE)
def on_game_start(data):
    """
    Start the game with the current registered players.
    """
    message_to_game(666, "game_started", {"message": "Game has started !"})
