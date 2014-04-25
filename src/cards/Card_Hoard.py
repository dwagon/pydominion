from Card import Card


class Card_Hoard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "Gain gold if buy victory"
        self.name = 'Hoard'
        self.playable = False
        self.gold = 2
        self.cost = 6

    def hook_buycard(self, game, player, card):
        """ When this is in play, when you buy a Victory card, gain a Gold """
        if card.isVictory():
            player.output("Gaining Gold from Hoard")
            player.addCard(game['Gold'].remove())

#EOF
