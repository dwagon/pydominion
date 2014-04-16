from Card import Card


class Card_Gardens(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.name = 'gardens'
        self.playable = False
        self.image = 'images/gardens.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

    def special_score(self, game, player):
        """ Worth 1VP for every 10 cards in your deck rounded down """
        numcards = len(self.discardpile + self.hand + self.deck)
        return int(numcards / 10)

#EOF
