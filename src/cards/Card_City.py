from Card import Card


class Card_City(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 action, more if stacks empty"
        self.name = 'City'
        self.cost = 5
        self.cards = 1
        self.actions = 2

    def special(self, game, player):
        """ If there are one or more empty Supply piles, +1 card.
        If there are two or more, +1 gold, +1 buy """
        empties = sum([1 for st in game.cardpiles if game[st].isEmpty()])
        if empties >= 1:
            player.t['cards'] += 1
        if empties >=2:
            player.t['gold'] += 1
            player.t['buys'] += 1

#EOF
