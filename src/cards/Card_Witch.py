from Card import Card


class Card_Witch(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 cards, curse everyone else"
        self.needcurse = True
        self.name = 'Witch'
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """ All other players gain a curse """
        for pl in game.players:
            if pl != player:
                if not pl.hasDefense():
                    player.output("%s got cursed" % pl.name)
                    pl.gainCard('curse')

#EOF
