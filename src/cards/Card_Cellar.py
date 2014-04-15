from Card import Card


class Card_Cellar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'cellar'
        self.image = 'images/cellar.jpg'
        self.action = 1
        self.cost = 2

    def special(self, game, player):
        """ Discard any number of cards, +1 card per card discarded """
        todiscard = []
        prompt = "Select which card(s) to discard?"
        while(1):
            options = [{'selector': '0', 'print': 'Discard no more', 'card': None}]
            index = 1
            for c in player.hand:
                s = "%s" % index
                discstr = "Undiscard" if c in todiscard else "Discard"
                options.append({'selector': s, 'print': '%s %s' % (c.name, discstr), 'card': c})
                index += 1
            o = player.userInput(options, prompt)
            if o['card'] == None:
                break
            if o['card'] in todiscard:
                todiscard.remove(o['card'])
            else:
                todiscard.append(o['card'])

        for c in todiscard:
            print "Discarding %s" % c.name
            player.addCard(c, 'discard')
            n = player.pickupCard()
            print "Picked up %s" % n.name

#EOF
