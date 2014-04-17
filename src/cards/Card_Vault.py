from Card import Card


class Card_Vault(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 cards, discard cards for +1 gold. Other players discard"
        self.name = 'Vault'
        self.image = 'images/vault.jpg'
        self.cost = 5
        self.cards = 2

    def special(self, game, player):
        """ Discard any number of cards. +1 Gold per card discarded.
            Each other player may discard 2 cards. If he does, he draws
            a card """
        print "Not implemented yet"


#EOF
