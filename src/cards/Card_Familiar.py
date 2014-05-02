from Card import Card


class Card_Familiar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'alchemy'
        self.desc = "+1 card, +1 action, curse everyone else"
        self.needcurse = True
        self.name = 'Familiar'
        self.cards = 1
        self.actions = 1
        self.cost = 3
        self.potcost = 1

    def special(self, game, player):
        """ All other players gain a curse """
        for pl in game.players:
            if pl != player:
                if not pl.hasDefense():
                    player.output("%s got cursed" % pl.name)
                    pl.gainCard('curse')

#EOF
