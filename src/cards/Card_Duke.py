from Card import Card


class Card_Duke(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'intrigue'
        self.desc = "Worth 1 per duchy"
        self.name = 'Duke'
        self.playable = False
        self.cost = 5

    def special_score(self, game, player):
        """ Worth 1VP per Duchy you have"""
        vp = 0
        for c in player.discardpile + player.hand + player.deck:
            if c.cardname == 'Duchy':
                vp += 1
        return vp

#EOF
