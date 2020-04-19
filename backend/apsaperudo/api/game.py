from apsaperudo.extensions import db
from apsaperudo.database.models import Game, GamePlayer
from apsaperudo.api.player import get_players_ids


def add_player_to_game(game_name, player_id):
    assert game_name in get_games_names()
    assert player_id in get_players_ids()
    game = Game.query.filter(Game.name == game_name).first()
    player = GamePlayer.query.get(player_id)
    player.game_id = game.id
    db.session.commit()


def remove_player_from_game(game_name, player_id):
    assert game_name in get_games_names()
    assert player_id in get_players_ids()
    player = GamePlayer.query.get(player_id)
    player.game_id = None
    db.session.commit()


def get_games_names():
    """
    Return a list of existing games ids.
    """
    return [i.name for i in Game.query.all()]


def get_games_ids():
    """
    Return a list of existing games ids.
    """
    return [i.id for i in Game.query.all()]
