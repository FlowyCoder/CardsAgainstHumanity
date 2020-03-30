class Player:
    id = 0
    name = ""
    hand = None
    points = 0

    def __init__(self, id, name, hand, points):
        self.id = id
        self.name = name
        self.hand = hand
        self.points = points

    def __repr__(self):
        return str(self.id) + self.name + str(self.hand) + str(self.points)
