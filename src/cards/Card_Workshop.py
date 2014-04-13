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

        for o in options:
            print "%s\t%s" % (o['selector'], o['print'])
        print "What card do you wish?",
        while(1):
            input = raw_input()
            for o in options:
                if o['selector'] == input:
                    player.discardCard(o['card'].remove())
                    print "Took %s" % o['card']
                    return
            print "Invalid Option (%s) - '0' to get nothing" % input

#EOF
