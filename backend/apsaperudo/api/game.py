from apsaperudo.extensions import db
from apsaperudo.database.models import Game, GamePlayer
from apsaperudo.api.player import get_players_ids


def get_games_ids():
    return [game.id for game in Game.query.all()]


def create_game(game_id):
    assert game_id not in get_games_ids()
    game = Game(id=game_id)
    db.session.add(game)
    db.session.commit()
    return game.id


def delete_game(game_id):
    assert game_id in get_games_ids()
    game = Game.query.get(game_id)
    db.session.delete(game)
    db.session.commit()


def add_player_to_game(game_id, player_id):
    assert player_id in get_players_ids()
    assert game_id in get_games_ids()
    player = GamePlayer.query.get(player_id)
    player.game_id = game_id
    db.session.commit()


def remove_player_from_game(game_id, player_id):
    assert game_id in get_games_ids()
    assert player_id in get_players_ids()
    player = GamePlayer.query.get(player_id)
    player.game_id = None
    db.session.commit()


def get_players_in_game(game_id):
    assert game_id in get_games_ids()
    return [
        player.id
        for player in GamePlayer.query.filter(GamePlayer.game_id == game_id)
    ]


def get_pending_games():
    return [
        game.id
        for game in GamePlayer.query.filter(GamePlayer.pending == True)
    ]
