from Card import Card


class Card_Militia(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'dominion'
        self.desc = "+2 gold, Every other player discards down to 3"
        self.name = 'Militia'
        self.gold = 2
        self.cost = 4

    def special(self, game, player):
        """ Every other player discards down to 3 cards """
        for plr in game.players:
            if plr == player:
                continue
            if plr.hasDefense(player):
                continue
            plr.output("Discard down to 3 cards")
            plr.plrDiscardDownTo(3)

#EOF
