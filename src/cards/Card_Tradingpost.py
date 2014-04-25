from Card import Card


class Card_Tradingpost(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash 2 cards for a silver"
        self.name = "Trading Post"
        self.cost = 5

    def special(self, game, player):
        """ Trash 2 card from your hand. If you do, gain a Silver card; put it into your hand"""
        trash = []
        player.output("Trash two cards")
        while(1):
            options = []
            if len(trash) in [0, 2]:
                options.append({'selector': '0', 'print': 'Finish trashing', 'card': None})
            index = 1
            for c in player.hand:
                sel = "%d" % index
                trashtag = 'Untrash' if c in trash else 'Trash'
                pr = "%s %s" % (trashtag, c.name)
                options.append({'selector': sel, 'print': pr, 'card': c})
                index += 1
            o = player.userInput(options, "Trash which card?")
            if not o['card']:
                break
            if o['card'] in trash:
                trash.remove(o['card'])
            else:
                trash.append(o['card'])

        if trash:
            for t in trash:
                player.output("Trashing %s" % t.name)
                player.trashCard(t)
            player.gainCard('silver', 'hand')
            player.t['gold'] += 2

#EOF
