#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Crew"""

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Crew(Card.Card):
    """Crew"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "+3 Cards; At the start of your next turn, put this onto your deck."
        self.cards = 3
        self.name = "Crew"
        self.cost = 5

    def duration(self, game, player):
        player.move_card(self, Piles.DECK)


###############################################################################
class TestCrew(unittest.TestCase):
    """Test Crew"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Crew", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Crew")

    def test_play(self):
        """Play a crew"""
        self.plr.add_card(self.card, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(
            len(self.plr.piles[Piles.HAND]), hand_size + 3 - 1
        )  # -1 for playing
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Crew", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
