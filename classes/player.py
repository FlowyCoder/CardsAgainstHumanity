class Player:

    def __init__(self, sid, name, hand = [], points = 0, spec = False):
        self.sid = sid
        self.name = name
        self.hand = hand
        self.points = points
        self.spectator = spec
        self.tempId = 0

    def __repr__(self):
        return str(self.sid) + self.name + str(self.hand) + str(self.points)