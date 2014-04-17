from Card import Card


class Card_Royalseal(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+2 gold. Cards gain go to top of deck"
        self.name = 'Royal Seal'
        self.image = 'images/royalseal.jpg'
        self.cost = 5
        self.gold = 2

    def special(self, game, player):
        """ While this is in play, when you gain a card, you may
            put that card on top of your deck"""
        print "Not implemented yet"


#EOF
