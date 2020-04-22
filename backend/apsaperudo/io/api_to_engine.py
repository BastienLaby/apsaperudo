from apsaperudo.database import models as db_models
from apsaperudo.engine import models as engine_models


def serialize_game(db_game):
    engine_game = engine_models.Game()
    engine_game.name = db_game.name
    engine_game.pending = db_game.pending
    return engine_game


