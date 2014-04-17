from Card import Card


class Card_Workersvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 actions, +1 buy"
        self.name = "Worker's Village"
        self.image = 'images/workersvillage.jpg'
        self.cost = 4
        self.cards = 1
        self.actions = 2
        self.buy = 1

#EOF
