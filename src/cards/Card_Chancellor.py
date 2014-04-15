from Card import Card


class Card_Chancellor(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'chancellor'
        self.image = 'images/chancellor.jpg'
        self.gold = 2
        self.cost = 3

    def special(self, game, player):
        """ You may immediately put your deck into your discard pile """
        options = [
            {'selector': '0', 'print': "Don't Discard Deck"},
            {'selector': '1', 'print': "Discard Deck"}
            ]

        for o in options:
            print "%s\t%s" % (o['selector'], o['print'])
        print "Chancellor: Discard deck? ",
        while(1):
            input = raw_input()
            if input == '0':
                return
            elif input == '1':
                # The equivalent of putting the deck into the discard
                # pile is putting the discard into the deck and
                # shuffling
                for c in player.discardpile[:]:
                    player.addCard(c, 'deck')
                player.shuffleDeck()
                return
            else:
                print "Invalid Option (%s) - '0' to do nothing" % input


#EOF
