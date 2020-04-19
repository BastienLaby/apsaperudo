from flask_socketio import emit

from apsaperudo.application import app

socketio = app.extensions["socketio"]


def message_to_player(message_type, message_data):
    message_data.update({
        "message_type": message_type
    })
    emit("server_message", message_data)


def message_to_game(message_type, message_data, game_id):
    message_data.update({
        "message_type": message_type
    })
    emit("server_message", message_data, room=game_id)


def message_to_all(message_type, message_data):
    message_data.update({
        "message_type": message_type
    })
    emit("server_message", message_data, broadcast=True)
