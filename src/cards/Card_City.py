from Card import Card


class Card_City(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 action, more if stacks empty"
        self.name = 'city'
        self.image = 'images/city.jpg'
        self.cost = 5
        self.card = 1
        self.action = 2

    def special(self, game, player):
        print "Not implemented yet"

#EOF
