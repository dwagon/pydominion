from Card import Card


class Card_Chapel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'chapel'
        self.image = 'images/chapel.jpg'
        self.cost = 2

    def special(self, game, player):
        """ Trash up to 4 cards from your hand """
        options = [{'selector': '0', 'print': 'No more trash', 'card': None}]
        index = 1
        for c in player.hand:
            selector = "%d" % index
            options.append({'selector': selector, 'print': "Trash %s" % c.name, 'card': c})
            index += 1
        trash = []
        print "Trash up to four cards"
        while(1):
            for o in options:
                trashtag = 'TRASHED' if o['card'] in trash else ''
                print "%s\t%s %s" % (o['selector'], o['print'], trashtag)
            print "Trash which card? ",
            input = raw_input()
            if input == '0':
                break
            for o in options:
                if input == o['selector']:
                    if o['card'] in trash:
                        trash.remove(o['card'])
                    else:
                        if len(trash) < 4:
                            trash.append(o['card'])
                        else:
                            print "Can only trash four cards"
        for t in trash:
            print "Trashing %s" % c.name
            player.trashCard(t)


#EOF
