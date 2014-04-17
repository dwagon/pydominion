from Card import Card


class Card_Rabble(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'TODO'
        self.desc = "TODO"
        self.name = 'rabble'
        self.image = 'images/rabble.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF
