from Card import Card


class Card_Venture(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+1 gold, get next treasure from deck"
        self.name = 'Venture'
        self.cost = 5

    def special(self, game, player):
        """ When you play this, reveal cards from your deck until
            you reveal a Treasure. Discard the other cards. Play that
            Treasure """
        while(1):
            c = player.pickupCard(verbose=False)
            if c.isTreasure():
                player.output("Picked up %s" % c.name)
                break
            else:
                player.output("Picked up and discarded %s" % c.name)
                player.t['gold'] -= c.gold    # Compensate for not keeping card
                player.discardCard(c)

#EOF
