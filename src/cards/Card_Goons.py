from Card import Card


class Card_Goons(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "Other players discard down to 3. +1 VP when buying"
        self.name = 'Goons'
        self.cost = 6
        self.buy = 1
        self.gold = 2

    def special(self, game, player):
        """ Each other player discards down to three cards """
        for plr in player.attackVictims():
            plr.output("Discard down to 3 cards")
            plr.plrDiscardDownTo(3)

    def hook_buyCard(self, game, player, card):
        """ While this card is in play, when you buy a card +1 VP """
        player.output("Scored 1 more from goons")
        player.addScore('goons', 1)

#EOF
