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
        copper = player.inHand('copper')
        if not copper:
            player.output("No coppers in hand")
            return
        options = []
        options.append({'selector': '0', 'print': "Don't trash a copper", 'trash': False})
        options.append({'selector': '1', 'print': "Trash a copper", 'trash': True})
        player.output("Trash a copper to gain +3 gold")
        o = player.userInput(options, "Trash a copper?")
        if o['trash']:
            player.trashCard(copper)
            player.t['gold'] += 3

#EOF
