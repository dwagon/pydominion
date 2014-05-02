from Card import Card


class Card_Transmute(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "Trash a card from hand to gain others"
        self.name = 'Transmute'
        self.cost = 0
        self.potcost = 1

    def special(self, game, player):
        """ Trash a card from your hand. If it is an...
            Action card, gain a Duchy, Treasure card, gain a Transmute,
            Victory card, gain a gold """
        player.output("Trash a card to gain...")
        options = []
        options.append({'selector': '0', 'print': 'Trash Nothing', 'card': None, 'gain': None})
        index = 1
        for c in player.hand:
            sel = "%d" % index
            if c.isAction():
                trashtag = 'Duchy'
            elif c.isTreasure():
                trashtag = 'Transmute'
            elif c.isVictory():
                trashtag = 'Gold'
            else:
                trashtag = 'Nothing'
            pr = "Trash %s for %s" % (c.name, trashtag)
            options.append({'selector': sel, 'print': pr, 'card': c, 'gain': trashtag})
            index += 1
        o = player.userInput(options, "Trash which card?")
        if not o['card']:
            return
        player.trashCard(o['card'])
        if o['gain'] != 'Nothing':
            player.gainCard(o['gain'])

#EOF
