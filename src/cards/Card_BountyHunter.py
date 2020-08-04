#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Bounty_Hunter """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Bounty_Hunter(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'menagerie'
        self.desc = """+1 Action; Exile a card from your hand. If you didn't
            have a copy of it in Exile, +3 Coin."""
        self.name = 'Bounty Hunter'
        self.cost = 4
        self.actions = 1

    def special(self, game, player):
        crd = player.cardSel(
            prompt="Exile a card",
            verbs=('Exile', 'Unexile')
        )
        if crd:
            if not player.in_exile(crd[0].name):
                player.addCoin(3)
            player.hand.remove(crd[0])
            player.exile_card(crd[0])


###############################################################################
class Test_Bounty_Hunter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bounty Hunter'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Bounty Hunter'].remove()

    def test_play(self):
        self.plr.set_exile('Copper')
        self.plr.setHand('Silver', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Exile Silver']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
