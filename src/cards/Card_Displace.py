#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Displace """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Displace(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = Game.MENAGERIE
        self.desc = """Exile a card from your hand. Gain a differently named card costing up to 2 Coin more than it."""
        self.name = 'Displace'
        self.cost = 5

    def special(self, game, player):
        crd = player.cardSel(
            prompt="Exile a card to gain a different one costing 2 more",
            verbs=('Exile', 'Unexile')
        )
        if crd:
            player.hand.remove(crd[0])
            player.exile_card(crd[0])
            player.plrGainCard(cost=crd[0].cost + 2, exclude=[crd[0].name])


###############################################################################
class Test_Displace(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Displace'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Displace'].remove()

    def test_playcard(self):
        """ Play a card """
        self.plr.setHand('Copper', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Exile Copper', 'Get Estate']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_exile('Copper'))
        self.assertIsNotNone(self.plr.in_discard('Estate'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
