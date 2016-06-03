#!/usr/bin/env python

from Card import Card


###############################################################################
class Card_Dameanna(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'knight']
        self.base = 'darkages'
        self.name = "Dame Anna"
        self.cost = 5

    def special(self, game, player):
        """ You may trash up to 2 cards form your hand.
        Each other player reveals the top 2 cards of his deck,
        trashes one of them consting from 3 to 6 and discards
        the rest. If a Knight is trashed by this, trash this
        card """
        for i in range(2):
            player.plrTrashCard()

        self.knight_special(game, player)

# EOF
