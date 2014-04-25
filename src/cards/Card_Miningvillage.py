from Card import Card


class Card_Miningvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 actions, trash self for +2 gold"
        self.name = 'Mining Village'
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def special(self, game, player):
        """ You may trash this card immediately. If you do +2 gold """
        options = [
            { 'selector': '0', 'print': 'Do nothing', 'trash': False },
            { 'selector': '1', 'print': 'Trash mining village for +2 gold', 'trash': True }
            ]
        o = player.userInput(options, "Choose one")
        if o['trash']:
            player.output("Trashing mining village")
            player.t['gold'] += 2
            player.trashCard(self)

#EOF
