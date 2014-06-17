from Card import Card


class Card_Royalseal(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+2 gold. Cards gain go to top of deck"
        self.playable = False
        self.name = 'Royal Seal'
        self.cost = 5
        self.gold = 2

    def hook_gainCard(self, game, player, card):
        """ While this is in play, when you gain a card, you may
            put that card on top of your deck"""
        mod = {}
        deck = player.plrChooseOptions(
            "Where to put %s?" % card.name,
            ("Put %s on discard" % card.name, False),
            ("Put %s on top of draw pile" % card.name, True))
        if deck:
            player.output("Putting %s on deck due to Royal Seal" % card.name)
            mod['destination'] = 'deck'
        return mod

#EOF
