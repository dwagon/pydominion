from Card import Card


class Card_Cutpurse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.desc = "+2 gold, other players discard copper"
        self.name = 'Cutpurse'
        self.gold = 2
        self.cost = 4

    def special(self, game, player):
        """ Each other player discard a Copper card (or reveals a
            hand with no copper)."""

        for victim in game.players:
            if victim == player:
                continue
            if victim.hasDefense(player):
                continue
            c = victim.inHand('Copper')
            if c:
                player.output("%s discarded a copper" % victim.name)
                victim.discardCard(c)

#EOF
