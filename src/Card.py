class Card(object):
    def __init__(self):
        self.image = None
        self.buys = 0
        self.cardtype = 'unknown'
        self.selectable = True
        self.actions = 0
        self.gold = 0
        self.cost = 0
        self.cards = 0
        self.victory = 0

    def special(self):
        pass

#EOF
