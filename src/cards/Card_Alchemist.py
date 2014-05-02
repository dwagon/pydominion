from Card import Card


class Card_Alchemist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+2 cards, +1 action; can put on top of deck if potion in play"
        self.name = 'Alchemist'
        self.cards = 2
        self.actions = 1
        self.cost = 3
        self.potcost = 1

    def special(self, game, player):
        """ When you discard this from play, you may put this on
            top of your deck if you have a Potion in play """
        for c in player.played:
            if c.name == 'Potion':
                break
        else:
            return
        print "Alchemist wonder powers activate"

#EOF
