from Card import Card


class Card_Monument(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "+2 gold, +1 VP"
        self.name = 'Monument'
        self.cost = 4
        self.gold = 2

    def special(self, game, player):
        player.addScore('monument', 1)

#EOF
