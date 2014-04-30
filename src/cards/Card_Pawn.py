from Card import Card


class Card_Pawn(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Choose two: +1 card, +1 action, +1 buy, +1 gold"
        self.name = 'Pawn'
        self.cost = 2

    def special(self, game, player):
        """ Choose two: +1 card; +1 action +1 buy; +1 gold. (The choices myst be different)"""
        selectable = {'card': '+1 card', 'action': '+1 action', 'buy': '+1 buy', 'gold': '+1 gold'}
        for i in range(2):
            options = []
            index = 0
            for k, v in selectable.items():
                options.append({'selector': '%d' % index, 'print': v, 'opt': k})
                index += 1
            o = player.userInput(options, "What do you want to do?")
            if o['opt'] == 'card':
                player.pickupCard()
            elif o['opt'] == 'action':
                player.t['actions'] += 1
            elif o['opt'] == 'buy':
                player.t['buys'] += 1
            elif o['opt'] == 'gold':
                player.t['gold'] += 1
            del selectable[o['opt']]

#EOF
