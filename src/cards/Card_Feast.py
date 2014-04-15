from Card import Card

class Card_Feast(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'feast'
        self.image = 'images/feast.jpg'
        self.cost = 4

    def special(self, game, player):
        """ Trash this card. Gain a card costing up to 5 """
        if self.trashCard(player):
            self.selectNewCard(game, player)

    def selectNewCard(self, game, player):
        print "Feast: Gain a card costing up to 5"
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        purchasable = game.cardsUnder(5)
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
                    player.addCard(o['card'].remove())
                    print "Took %s" % o['card'].name
                    return
            print "Invalid Option (%s) - '0' to get nothing" % input

    def trashCard(self, player):
        options = [
            {'selector': '0', 'print': "Don't trash this card"},
            {'selector': '1', 'print': "Trash this card"}
            ]
        for o in options:
            print "%s\t%s" % (o['selector'], o['print'])
        print "Trash this card? ",
        while(1):
            input = raw_input()
            if input == '0':
                return False
            elif input == '1':
                player.trashCard(self)
                return True
            else:
                print "Invalid Option (%s) - '0' to do nothing"


#EOF
