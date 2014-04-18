from Card import Card


class Card_Militia(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 gold, Every other player discards down to 3"
        self.name = 'Militia'
        self.gold = 2
        self.cost = 4

    def special(self, game, player):
        """ Every other player discards down to 3 cards """
        for plr in game.players:
            if plr == player:
                continue
            if plr.hasDefense():
                print "Player %s is defended" % plr.name
                continue
            print "*" * 20
            print "Player %s discard down to %d cards" % (plr.name, 3)
            plr.discardDownTo(3)
        print "*" * 20
        print "Back to %s" % player.name

#EOF
