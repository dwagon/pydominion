from Card import Card


class Card_Councilroom(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+4 cards, +1 buy. Everyone else +1 card"
        self.name = 'Council Room'
        self.cards = 4
        self.buys = 1
        self.cost = 5

    def special(self, game, player):
        """ Each other player draws a card """
        for pl in game.players:
            if pl != player:
                pl.pickupCard()

#EOF
