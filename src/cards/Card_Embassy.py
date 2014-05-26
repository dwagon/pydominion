from Card import Card


class Card_Embassy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+5 Cards, Discard 3. Everyone gets a silver on purchase"
        self.name = 'Embassy'
        self.cost = 5
        self.cards = 5

    def special(self, game, player):
        player.plrDiscardCards(3)

    def hook_gainThisCard(self, game, player):
        """ When you gain this, each other player gains a Silver """
        for plr in game.players:
            if plr != player:
                plr.output("Gained a silver from %s's purchase of Embassy" % player.name)
                plr.gainCard('Silver')

#EOF
