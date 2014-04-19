from Card import Card


class Card_Mine(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a treasure, gain a better treasure"
        self.name = 'Mine'
        self.cost = 5

    def special(self, game, player):
        """ Trash a treasure card from your hand. Gain a treasure card
            costing up to 3 more, put it in your hand """
        options = [{'selector': '0', 'print': "Don't trash a card", 'card': None}]
        index = 1
        for c in player.hand:
            if c.isTreasure():
                sel = "%s" % index
                options.append({'selector': sel, 'print': "Trash %s" % c.name, 'card': c})
                index += 1
        print "Trash a treasure to gain a better one"
        o = player.userInput(options, "Trash which treasure?")
        if o['card']:
            val = o['card'].cost
            # Make an assumption and pick the best treasure card
            for tc in game.baseCards:
                if game[tc].cost == val + 3:
                    c = player.gainCard(c, 'hand')
                    print "Converted to %s" % c.name
                    player.trashCard(o['card'])
                    player.t['gold'] += c.gold
                    break
            else:
                print "No appropriate treasure card exists"

#EOF
