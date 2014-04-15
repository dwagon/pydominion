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
        trash = []
        print "Trash up to four cards"
        while(1):
            options = [{'selector': '0', 'print': 'No more trash', 'card': None}]
            index = 1
            for c in player.hand:
                selector = "%d" % index
                trashtag = 'Untrash' if c in trash else 'Trash'
                options.append({'selector': selector, 'print': "%s %s" % (trashtag, c.name), 'card': c})
                index += 1
            o = player.userInput(options, "Trash which card")
            if not o['card']:
                break
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
