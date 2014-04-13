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
        options = [{'selector': '0', 'print': 'Discard no more', 'card': None}]
        todiscard = []
        index = 1
        for c in player.hand:
            s = "%s" % index
            options.append({'selector': s, 'print': 'Discard %s' % c.name, 'card': c})
            index += 1

        for o in options:
            print "%s\t%s" % (o['selector'], o['print'])
        while(1):
            print "Select which card(s) to discard?",
            input = raw_input()
            good = False
            if input == '0':
                break
            for o in options:
                if o['selector'] == input:
                    good = True
                    if o['card'] in todiscard:
                        todiscard.remove(o['card'])
                    else:
                        todiscard.append(o['card'])
                    break
            if not good:
                print "Invalid Option (%s) - '0' to stop discarding" % input

        for c in todiscard:
            print "Discarding %s" % c.name
            player.addCard(c, 'discard')
            n = player.pickupCard()
            print "Picked up %s" % n.name

#EOF
