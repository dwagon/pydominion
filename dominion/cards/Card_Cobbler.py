#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Cobbler"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Cobbler(Card.Card):
    """Cobbler"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "At the start of your next turn, gain a card to your hand costing up to 4."
        self.name = "Cobbler"
        self.cost = 5

    def duration(self, game, player):
        player.plr_gain_card(4)


###############################################################################
class Test_Cobbler(unittest.TestCase):
    """Test Cobbler"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Cobbler", "Moat"],
            badcards=["Blessed Village", "Cemetery"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Cobbler"].remove()

    def test_duration(self):
        """Test Playing Cobbler"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.test_input = ["Get Moat"]
        self.plr.start_turn()
        self.assertLessEqual(self.plr.discardpile[0].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
