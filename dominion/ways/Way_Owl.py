#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Owl"""

import unittest
from dominion import Card
from dominion import Game
from dominion import Way


###############################################################################
class Way_Owl(Way.Way):
    """Way of the Owl"""

    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Draw until you have 6 cards in hand."
        self.name = "Way of the Owl"

    def special_way(self, game, player, card):
        num = 6 - player.hand.size() + 1  # for the card that is used
        player.output(f"Picking up {num} cards from Way of the Owl")
        player.pickup_cards(num=num)


###############################################################################
class Test_Owl(unittest.TestCase):
    """Test Way of the Owl"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            waycards=["Way of the Owl"],
            initcards=["Cellar"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Cellar"].remove()
        self.way = self.g.ways["Way of the Owl"]

    def test_play(self):
        """Perform a Owl"""
        self.plr.hand.set("Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.g.print_state()
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
