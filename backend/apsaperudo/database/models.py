from apsaperudo.extensions import db


def clear_db():
    Game.query.delete()
    GamePlayer.query.delete()
    db.session.commit()


class Game(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    pending = db.Column(db.Boolean())

    def __repr__(self):
        return f"<Game {self.id}>"


class GamePlayer(db.Model):
    id = db.Column(db.String(64), primary_key=True)  # socket session id
    name = db.Column(db.String(64))
    game_id = db.Column(db.String(64))  # foreign key
    pending = db.Column(db.Boolean())

    def __repr__(self):
        return f'{"--> " if self.is_current else ""}<Player {self.name}#{self.id}>'
