#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_BandOfMisfits(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_COMMAND]
        self.base = Game.DARKAGES
        self.desc = """Play a non-Command Action card from the Supply that costs
            less than this, leaving it there."""
        self.name = "Band of Misfits"
        self.cost = 5

    def special(self, game, player):
        actionpiles = game.getActionPiles(self.cost - 1)
        actions = player.cardSel(
            prompt="What action card do you want to play?", cardsrc=actionpiles
        )
        player.card_benefits(actions[0])


###############################################################################
class Test_BandOfMisfits(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            initcards=["Band of Misfits", "Village", "Bureaucrat", "Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Band of Misfits"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_market(self):
        """Make the Band of Misfits be a Bureaucrat"""
        self.plr.test_input = ["Bureaucrat"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_deck("Silver"))

    def test_play_feast(self):
        """Make the Band of Misfits be a Village"""
        self.plr.test_input = ["Select Village"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
