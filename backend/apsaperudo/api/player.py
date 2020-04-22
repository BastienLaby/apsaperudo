from apsaperudo.database.models import GamePlayer
from apsaperudo.extensions import db


def get_players_ids():
    return [player.id for player in GamePlayer.query.all()]


def create_player(player_id):
    assert player_id not in get_players_ids()
    player = GamePlayer(id=player_id)
    db.session.add(player)
    db.session.commit()


def delete_player(player_id):
    assert player_id in get_players_ids()
    player = GamePlayer.query.get(player_id)
    db.session.delete(player)
    db.session.commit()


def set_player_id(player_id, new_player_id):
    existing_ids = get_players_ids()
    assert player_id in existing_ids
    assert new_player_id not in existing_ids
    player = GamePlayer.query.get(player_id)
    player.id = new_player_id
    db.session.commit()


def get_player_game(player_id):
    assert player_id in get_players_ids()
    return GamePlayer.query.get(player_id).game_id
