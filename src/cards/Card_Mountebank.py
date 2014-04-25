from Card import Card


class Card_Mountebank(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 gold. Others discard curse or gain one + copper"
        self.name = 'Mountebank'
        self.needcurse = True
        self.gold = 2
        self.cost = 5

    def special(self, game, player):
        """ Each other player may discard a Curse. If he doesnt, he gains a Curse and a Copper """
        for plr in game.players:
            if plr == player:
                continue
            if plr.hasDefense():
                print("Player %s is defended" % plr.name)
                continue
            for c in plr.hand:
                if c.cardname == 'curse':
                    print("Player %s trashed a curse" % plr.name)
                    plr.trashCard(c)
                    break
            else:
                print("Player %s gained a curse and a copper" % plr.name)
                plr.addCard(game['Curse'].remove())
                plr.addCard(game['Copper'].remove())

#EOF
