from apsaperudo.database.models import GamePlayer
from apsaperudo.extensions import db


def get_players_ids():
    players_ids = GamePlayer.query.all()
    return [i.id for i in players_ids]


def create_player(player_id):
    assert player_id not in get_players_ids()
    player = GamePlayer(id=player_id)
    db.session.add(player)
    db.session.commit()
