from Card import Card


class Card_Philosophersstone(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'alchemy'
        self.desc = "Gain +1 Gold for every 5 cards owned"
        self.name = "Philosopher's Stone"
        self.cost = 3
        self.playable = False
        self.potcost = 1

    def hook_goldvalue(self, game, player):
        """ When you play this, count your deck and discard pile.
            Worth 1 per 5 cards total between them (rounded down) """
        numcards = len(player.deck) + len(player.discardpile)
        extragold = numcards / 5
        return extragold

#EOF
