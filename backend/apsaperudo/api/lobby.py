
from apsaperudo.database.models import GamePlayer
from apsaperudo.extensions import db


def create_pending_player(player_id, player_name):
    assert player_name not in get_pending_players_names()
    player = GamePlayer(id=player_id, name=player_name, pending=True)
    db.session.add(player)
    db.session.commit()
    return player.id


def get_pending_players_ids():
    return [i.id for i in GamePlayer.query.filter(GamePlayer.pending == True)]


def get_pending_players_names():
    return [i.name for i in GamePlayer.query.filter(GamePlayer.pending == True)]


def rename_pending_player(player_id, new_name):
    assert player_id in get_pending_players_ids()
    assert new_name not in get_pending_players_names()
    player = GamePlayer.query.get(player_id)
    player.name = new_name
    db.session.commit()
    return new_name


def delete_pending_player(player_id):
    # assert player_id in get_pending_players_ids()
    player = GamePlayer.query.get(player_id)
    db.session.delete(player)
    db.session.commit()
    return player.name  # still valid after .remove() ?
