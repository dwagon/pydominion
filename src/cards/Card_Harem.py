from Card import Card


class Card_Harem(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'harem']
        self.base = 'intrigue'
        self.desc = "2 VPs"
        self.name = 'Harem'
        self.gold = 2
        self.victory = 2
        self.cost = 6

#EOF
