

class Game(object):

    name = ""
    players = []
    pending = True


class Player(object):

    name = ""
    dices = []


class Dice(object):

    value = 1  # [1, 2, 3, 4, 5, 6]
    alive = True
