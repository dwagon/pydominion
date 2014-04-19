from Card import Card


class Card_Goons(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Other players discard down to 3. +1 VP when buying"
        self.name = 'Goons'
        self.cost = 6
        self.buy = 1
        self.gold = 2

    def special(self, game, player):
        """ Each other player discards down to three cards """
        for plr in game.players:
            if plr == player:
                continue
            if plr.hasDefense():
                print "Player %s is defended" % plr.name
                continue
            print "*" * 20
            print "Player %s discard down to %d cards" % (plr.name, 3)
            plr.plrDiscardDownTo(3)
        print "*" * 20
        print "Back to %s" % player.name

    def hook_buycard(self, game, player, card):
        """ While this card is in play, when you buy a card +1 VP """
        print "Scored 1 more from goons"
        player.basescore += 1

#EOF
