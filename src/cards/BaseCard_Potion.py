from Card import Card


class Card_Potion(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'alchemy'
        self.basecard = True
        self.playable = False
        self.desc = "+1 potion"
        self.name = 'Potion'
        self.potion = 1
        self.cost = 4

# EOF
