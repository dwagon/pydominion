#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Band_of_misfits"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_BandOfMisfits(Card.Card):
    """Band of Misfits"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.COMMAND]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Play a non-Command Action card from the Supply that costs
            less than this, leaving it there."""
        self.name = "Band of Misfits"
        self.cost = 5

    def special(self, game, player):
        actionpiles = game.getActionPiles(self.cost - 1)
        actions = player.card_sel(
            prompt="What action card do you want to play?", cardsrc=actionpiles
        )
        player.card_benefits(actions[0])


###############################################################################
class Test_BandOfMisfits(unittest.TestCase):
    """Test Band of Misfits"""

    def setUp(self):
        self.g = Game.TestGame(
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
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.deck)

    def test_play_feast(self):
        """Make the Band of Misfits be a Village"""
        self.plr.test_input = ["Select Village -"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
