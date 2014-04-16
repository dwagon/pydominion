from Card import Card


class Card_Silver(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+2 gold"
        self.playable = False
        self.name = 'silver'
        self.image = 'images/silver.jpg'
        self.gold = 2
        self.cost = 3

#EOF
