from Card import Card


class Card_Greathall(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'victory']
        self.base = 'intrigue'
        self.desc = "+1 card, +1 action, 1VP"
        self.name = 'Great Hall'
        self.cost = 5
        self.cards = 1
        self.actions = 1

    def special_score(self, game, player):
        return 1

#EOF
