from Card import Card


class Card_Nobles(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "2VP, choose +3 cards or +2 actions"
        self.name = 'Nobles'
        self.victory = 2
        self.cost = 6

    def special(self, game, player):
        """ Choose one: +3 Cards; or +2 Actions """
        options = [
            {'selector': '0', 'print': '+3 Cards', 'choose': 'cards'},
            {'selector': '1', 'print': '+2 Actions', 'choose': 'actions'}
            ]
        o = player.userInput(options, "Choose one")
        if o['choose'] == 'cards':
            for i in range(3):
                player.pickupCard()
            return
        if o['choose'] == 'actions':
            player.t['actions'] += 2

#EOF
