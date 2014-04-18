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
            self.playerDiscard(plr)
        print "*" * 20
        print "Back to %s" % player.name

    def playerDiscard(self, plr):
        print "*" * 20
        print "Player %s discard down to three cards" % plr.name
        discard = []
        while(1):
            options = []
            numleft = (len(plr.hand) - len(discard)) - 3
            if numleft == 0:
                options = [{'selector': '0', 'print': 'Finished selecting', 'card': None}]
            index = 1
            for c in plr.hand:
                sel = "%s" % index
                pr = "%s %s" % ("Undiscard" if c in discard else "Discard", c.name)
                options.append({'selector': sel, 'print': pr, 'card': c})
                index += 1

            numleft = (len(plr.hand) - len(discard)) - 3
            o = plr.userInput(options, "Discard %s more cards." % numleft)
            if o['card']:
                if o['card'] in discard:
                    discard.remove(o['card'])
                else:
                    discard.append(o['card'])
            numleft = (len(plr.hand) - len(discard)) - 3
            if o['card'] is None and numleft == 0:
                break
        for c in discard:
            plr.discardCard(c)

#EOF
