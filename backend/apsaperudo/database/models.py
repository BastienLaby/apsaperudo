from apsaperudo.extensions import db


def clear_db():
    pass


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turn = db.Column(db.Integer)

    def __repr__(self):
        return f"<Game {self.id}>"


class GamePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    is_current = db.Column(db.Boolean)
    round_idx = db.Column(db.Integer, default=0)
    game_id = db.Column(db.Integer)  # foreign key

    def __repr__(self):
        return f'{"--> " if self.is_current else ""}<Player {self.name}#{self.id}>'
