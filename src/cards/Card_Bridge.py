from Card import Card


class Card_Bridge(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 buy, +1 gold, all cards -1 cost"
        self.name = 'Bridge'
        self.buys = 1
        self.gold = 1
        self.cost = 4

    def hook_cardCost(self, game, player, card):
        """ All cards (including cards in players' hands) cost 1
            less this turn, but not less than 0 """
        if self in player.played:
            return -1
        return 0
#EOF
