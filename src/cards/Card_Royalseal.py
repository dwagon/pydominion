from Card import Card


class Card_Royalseal(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'TODO'
        self.desc = "TODO"
        self.name = 'royalseal'
        self.image = 'images/royalseal.jpg'
        self.cost = 4

    def special(self, game, player):
        pass


#EOF
