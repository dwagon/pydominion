from Card import Card


class Card_Witch(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.needcurse = True
        self.name = 'witch'
        self.image = 'images/witch.jpg'
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """ All other players gain a curse """
        cursepile = game['Curse']
        for pl in game.players:
            if pl != player:
                if pl.hasDefense():
                    print "%s's moat blocked curse" % pl.name
                else:
                    print "%s got cursed" % pl.name
                    pl.addCard(cursepile.remove())

#EOF
