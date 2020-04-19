from apsaperudo.extensions import db
from apsaperudo.database.models import Game, GamePlayer
from apsaperudo.api.player import get_players_ids


def create_game(game_id):
    """
    Create a game in database and return its id.
    """
    assert game_id not in get_games()
    game = Game(id=game_id)
    db.session.add(game)
    db.session.commit()


def add_player_to_game(game_id, player_id):
    """
    """
    assert game_id in get_games()
    assert player_id in get_players_ids()
    player = GamePlayer.query.get(GamePlayer.id == player_id)
    player.game_id = game_id
    db.session.commit()


def remove_player_from_game(game_id, player_id):
    """
    """
    assert game_id in get_games()
    assert player_id in get_players_ids()
    player = GamePlayer.query.get(GamePlayer.id == player_id)
    player.game_id = None
    db.session.commit()


def get_games():
    """
    Return a list of existing games ids.
    """
    return [i.id for i in Game.query.all()]
