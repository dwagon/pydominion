from Card import Card


class Card_Talisman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+1 gold. Gain copy of non-victory cards you buy"
        self.name = 'Talisman'
        self.playable = False
        self.cost = 4
        self.gold = 1

    def hook_buyCard(self, game, player, card):
        """ While this is in play, when you buy a card costing 4
            or less that is not a victory card, gain a copy of it."""
        if card.cost <= 4 and not card.isVictory():
            player.output("Gained another %s from Talisman" % card.name)
            player.addCard(game[card.cardname].remove())

#EOF
