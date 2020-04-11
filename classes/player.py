class Player:
    sid = 0
    name = ""
    hand = []
    points = 0
    spectator = False

    def __init__(self, sid, name, hand, points, spec):
        self.sid = sid
        self.name = name
        self.hand = hand
        self.points = points
        self.spectator = spec

    def __repr__(self):
        return str(self.sid) + self.name + str(self.hand) + str(self.points)

    def get_json(self):
        return "{'sid' : '" + self.sid + "', 'name' : '" + self.name + "'}"
