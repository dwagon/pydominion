from Card import Card


class Card_Conspirator(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 gold. If played more than 3 actions +1 card, +1 action"
        self.name = 'Conspirator'
        self.gold = 2
        self.cost = 4

    def special(self, player, game):
        """ If you've player 3 or more actions this turn (counting
            this); +1 card, +1 action """
        if player.turnstats['actions'] >= 3:
            player.pickupCard()
            player.t['actions'] += 1

#EOF
