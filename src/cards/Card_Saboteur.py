from Card import Card


class Card_Saboteur(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash other players cards but they get one back"
        self.name = 'Saboteur'
        self.cost = 5

    def special(self, game, player):
        """ Each other player reveals cards from the top of his
            deck until revealing one costing 3 or more. He trashes that
            card and may gain a card costing at most 2 less than it.
            He discards the other revealed cards. """
        for victim in game.players:
            if victim != player:
                continue
            if victim.hasDefense():
                continue
            card = self.pickCard(victim)
            victim.output("Trashing %s" % card.name)
            victim.trashCard(card)
            victim.plrGainCard(card.cost - 2)

    def pickCard(self, victim):
        while(1):
            c = victim.pickupCard()
            if c.cost >= 3:
                return c
            victim.output("Discarding %s" % c.name)
            victim.discardCard(c)

#EOF
