from Card import Card


class Card_Workshop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'workshop'
        self.image = 'images/workshop.jpg'
        self.cost = 3

    def special(self, game, player):
        """ Gain a card costing up to 4"""
        print "Workshop: Gain a card costing up to 4"
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        purchasable = game.cardsUnder(4)
        index = 1
        for p in purchasable:
            selector = "%d" % index
            toprint = 'Get %s (%d gold)' % (p.name, p.cost)
            options.append({'selector': selector, 'print': toprint, 'card':p})
            index += 1

        o = player.userInput(options, "What card do you wish?")
        player.addCard(o['card'].remove())
        print "Took %s" % o['card']

#EOF
