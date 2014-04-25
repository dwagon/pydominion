from Card import Card


class Card_Grandmarket(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "+1 card, +1 action, +1 buy, +2 gold"
        self.name = 'Grand Market'
        self.cost = 6
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.gold = 2

    def hook_allowedtobuy(self, game, player):
        """ You can't buy this if you have any copper in play """
        for c in player.hand:
            if c.name == 'Copper':
                print("Not allowed to buy Grand Market due to copper in hand")
                return False
        return True

#EOF
