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

    def hook_gaincard(self, game, player, card):
        """ While this is in play, when you gain a card, you may
            put that card on top of your deck"""
        mod = {}
        options = []
        options.append({'selector': '0', 'print': "Put %s on discard" % card.name, 'deck': False})
        options.append({'selector': '1', 'print': "Put %s on top of draw pile" % card.name, 'deck': True})
        o = player.userInput(options, "Where to put %s?" % card.name)
        if o['deck']:
            player.output("Putting %s on deck due to Royal Seal" % card.name)
            mod['destination'] = 'deck'
        return mod

#EOF
