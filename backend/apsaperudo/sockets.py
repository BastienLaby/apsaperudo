from flask import request
from flask_socketio import join_room, leave_room, rooms
from faker import Faker

from apsaperudo.application import app
from apsaperudo.api.game import (
    get_games_ids,
    create_game,
    delete_game,
    add_player_to_game,
    remove_player_from_game,
    get_players_in_game,
)
from apsaperudo.api.player import (
    get_players_ids,
    create_player,
    delete_player,
    set_player_id
)
from apsaperudo.io.messages import (
    message_to_player, message_to_game, message_to_all
)


socketio = app.extensions["socketio"]
_namespace = "/apsaperudo"
_connected_clients = 0
_player_id_per_sid = {}


def get_client_player_id():
    assert request.sid in _player_id_per_sid
    return _player_id_per_sid[request.sid]


def set_client_player_id(player_id):
    _player_id_per_sid[request.sid] = player_id


class PseudoGenerationAttemptsExceeded(Exception):
    pass


@socketio.on("connect", namespace=_namespace)
def connect_handler():
    """
    Received when the player enters the lobby.
    Create a random default player_id.
    Return events to the user indicating the successfull connection and the game list.
    """

    fake = Faker()
    attempts = 1000
    existing_players = get_players_ids()
    for i in range(attempts):
        player_id = fake.name()
        if player_id not in existing_players:
            break
    else:
        raise PseudoGenerationAttemptsExceeded()

    create_player(player_id)
    set_client_player_id(player_id)

    message_to_player("connection_ok", {
        "message": "Connected !",
        "player_id": player_id
    })
    message_to_player("games_updated", {
        "message": "Games list updated.",
        "games": get_games_ids()
    })


@socketio.on("disconnect", namespace=_namespace)
def disconnect_handler():
    """
    Received when the socket is removed or if the client closes the tab.
    Remove the client from every game and room he's in.
    """
    player_id = get_client_player_id()
    for room in rooms()[1:]:
        on_game_leave({"game_id": room, "player_id": player_id})
    delete_player(player_id)


@socketio.on("change_player_id", namespace=_namespace)
def on_player_id_change(data):
    """
    Received when the user changes its player_id.
    Check if a  player with the same name already exists.
        If that's the case, return a "already_taken_player_id" event.
        Else, rename the player and return a "player_id_changed" event.
    """
    assert "new_player_id" in data
    new_id = data["new_player_id"]
    if new_id in get_players_ids():
        message_to_player("already_taken_player_id", {
            "message": f"player_id \"{new_id}\" already taken."
        })
    else:
        set_player_id(get_client_player_id(), new_id)
        message_to_player("player_id_changed", {
            "message": f"player_id changed to #{new_id}.",
            "player_id": new_id
        })
        set_client_player_id(new_id)


@socketio.on("create_game", namespace=_namespace)
def on_game_create(data):
    """
    Create a new game with the given name.
    If a game with the same name exists, return a "already_taken_gamename" event.
    Else, create the game, return a "game_created" event, and make the player join it.
    """
    assert "game_id" in data
    game_id = data["game_id"]
    if game_id in get_games_ids():
        message_to_player("already_taken_gamename", {
            "message": f"Game name \"{game_id}\" already taken."
        })
    else:
        create_game(game_id)
        message_to_player("game_created", {
            "message": f"Game #{game_id} created."
        })
        message_to_all("games_updated", {
            "message": "Games list updated.",
            "games": get_games_ids()
        })
        on_game_join(data)


@socketio.on("join_game", namespace=_namespace)
def on_game_join(data):
    """
    Join a player to a game. Add it in the corresponding sockets room.
    Send a "already_in_game" event if the player is already in the game.
    If the player is in other games, remove it from them.
    Send a "game_joined" event to the player, and a "player_joined" event to the room.
    """
    assert "game_id" in data
    game_id = data["game_id"]
    player_id = get_client_player_id()

    if game_id in rooms():
        message_to_player("already_in_game", {
            "message": f"You are already in game #{game_id}.",
            "game_id": game_id
        })
        return

    # disconnect from every rooms
    for room in rooms()[1:]:
        on_game_leave({"game_id": room, "player_id": player_id})

    # join the new game
    add_player_to_game(game_id, player_id)
    join_room(game_id)
    message_to_player("game_joined", {
        "message": f"You entered #{game_id}.",
        "game_id": game_id
    })
    message_to_game("player_joined", {
            "message": f"#{player_id} entered the game."
        }, game_id
    )


@socketio.on("leave_game", namespace=_namespace)
def on_game_leave(data):
    """
    Make the client leave a given game.
    If the game is empty, delete it.
    Send a "game_leaved" event to the client and a "player_leaved" event to the room.
    """
    assert "game_id" in data
    player_id = get_client_player_id()
    game_id = data["game_id"]

    leave_room(game_id)
    remove_player_from_game(game_id, player_id)
    if not get_players_in_game(game_id):
        delete_game(game_id)
        message_to_all("games_updated", {
            "message": "Games list updated.",
            "games": get_games_ids()
        })

    message_to_player("game_leaved", {
        "message": f"You left #{game_id}",
        "game_id": game_id
    })
    message_to_game("player_leaved", {
            "message": f"#{player_id} left the game"
        }, data["game_id"]
    )
