from Card import Card


class Card_Moneylender(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Trash a copper from hand for +3 gold"
        self.name = 'Money Lender'
        self.cost = 4

    def special(self, game, player):
        """ Trash a copper card from your hand. If you do +3 Gold """
        for c in player.hand:
            print c.cardname
            if c.cardname == 'copper':
                copper = c
                break
        else:
            print "No coppers in hand"
            return
        options = []
        options.append({'selector': '0', 'print': "Don't trash a copper", 'trash': False})
        options.append({'selector': '1', 'print': "Trash a copper", 'trash': True})
        print "Trash a copper to gain +3 gold"
        o = player.userInput(options, "Trash a copper?")
        if o['trash']:
            player.trashCard(copper)
            player.t['gold'] += 3

#EOF
