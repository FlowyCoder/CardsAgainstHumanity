class Player:
    id = 0
    name = ""
    hand = []
    points = 0
    spectator = False

    def __init__(self, id, name, hand, points, spec):
        self.id = id
        self.name = name
        self.hand = hand
        self.points = points
        self.spectator = spec

    def __repr__(self):
        return str(self.id) + self.name + str(self.hand) + str(self.points)

    def get_json(self):
        return "{'id' : '" + self.id + "', 'name' : '" + self.name + "'}"
