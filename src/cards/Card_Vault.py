from Card import Card


class Card_Vault(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "TODO"
        self.name = 'vault'
        self.image = 'images/vault.jpg'
        self.cost = 4

    def special(self, game, player):
        pass


#EOF
