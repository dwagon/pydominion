from Card import Card


class Card_Apprentice(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 action, Trash a card, +1 card per cost, +2 cards if it is a potion"
        self.name = 'Apprentice'
        self.cost = 5
        self.actions = 1

    def special(self, game, player):
        """ Trash a card from your hand. +1 Card per gold it costs.
            +2 Cards if it has potion it its cost """
        c = player.plrTrashCard()
        numcards = c.cost
        if c.potcost:
            numcards += 2
        for c in range(numcards):
            player.pickupCard()


#EOF
