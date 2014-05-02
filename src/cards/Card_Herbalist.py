from Card import Card


class Card_Herbalist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+1 buy, +1 gold, can put treasures on top of deck"
        self.name = 'Herbalist'
        self.cost = 2
        self.buys = 1
        self.gold = 1

    def special(self, game, player):
        """ When you discard this from play, you may put one of
            your Treasures from play on top of your deck """
        # TODO

#EOF
