from Card import Card


class Card_City(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 action, more if stacks empty"
        self.name = 'City'
        self.cost = 5
        self.card = 1
        self.action = 2

    def special(self, game, player):
        """ If there are one or more empty Supply piles, +1 card.
        If there are two or more, +1 gold, +1 buy """
        print "Not implemented yet"

#EOF
