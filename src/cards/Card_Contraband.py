from Card import Card


class Card_Contraband(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+3 gold, +1 buy, player to left bans a card purchase"
        self.name = 'contraband'
        self.image = 'images/contraband.jpg'
        self.cost = 5
        self.gold = 3
        self.buy = 1

    def special(self, game, player):
        pass

#EOF
