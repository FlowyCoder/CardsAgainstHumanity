class Cards:
    text = ""

    def __init_(self):
        self.text = ""

    def __init__(self, cardString):
        self.text = cardString


class BlackCard(Cards):
    pick = 0

    def __init__(self, text, pick):
        super().__init__(text)
        self.pick = pick


class WhiteCard(Cards):
    pass
