#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Zombie_Mason(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'zombie']
        self.base = 'nocturne'
        self.desc = "Trash the top card of your deck. You may gain a card costing up to 1 more than it."
        self.name = 'Zombie Mason'
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1

    def setup(self, game):
        game.trashpile.add(self)

    def special(self, game, player):
        topdeck = player.nextCard()
        player.trashCard(topdeck)
        player.output("Trashed {} from the top of your deck".format(topdeck.name))
        player.plrGainCard(topdeck.cost + 1)


###############################################################################
class Test_Zombie_Mason(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Zombie Mason', 'Guide'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Zombie Mason'].remove()

    def test_play(self):
        self.plr.setDeck('Estate')
        self.plr.test_input = ['Guide']
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertIsNotNone(self.g.in_trash('Estate'))
        self.assertIsNotNone(self.plr.inDiscard('Guide'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
