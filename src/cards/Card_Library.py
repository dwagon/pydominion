from Card import Card


class Card_Library(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Draw up to 7 cards"
        self.name = 'Library'
        self.cost = 5

    def special(self, game, player):
        """ Draw until you have 7 cards in your hand. You may set
        aside action cards drawn this way, as you draw them; discard
        the set aside cards after you finish drawing """
        pass

#EOF
