from Card import Card


class Card_Talisman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'TODO'
        self.desc = "TODO"
        self.name = 'talisman'
        self.image = 'images/talisman.jpg'
        self.cost = 4

    def special(self, game, player):
        pass


#EOF
