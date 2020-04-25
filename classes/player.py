class Player:

    def __init__(self, sid, name, points = 0, spec = False):
        self.sid = sid
        self.name = name
        self.hand = []
        self.points = points
        self.spectator = spec
        self.tempId = 0
        self.deleted_card = False

    def to_json(self):
        return {
            'sid': self.sid,
            'name': self.name,
            'hand': self.hand,
            'points': self.points,
            'spectator': self.spectator,
            'tempId': self.tempId,
            'deleted_card': self.deleted_card
        }