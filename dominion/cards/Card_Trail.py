#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Trail"""

import unittest
from dominion import Game, Card, Piles
from dominion.Player import Phase


###############################################################################
class Card_Trail(Card.Card):
    """Trail"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+1 Card; +1 Action; 
        When you gain, trash, or discard this, other than in Clean-up, you may play it."""
        self.cards = 1
        self.actions = 1
        self.name = "Trail"
        self.cost = 4

    def hook_gain_this_card(self, game, player):
        if self.want_to_play(player):
            player.play_card(self, cost_action=False, discard=False)
            return {"destination": Piles.PLAYED}

    def hook_discard_this_card(self, game, player, source):
        if player.phase != Phase.CLEANUP:
            if self.want_to_play(player):
                player.play_card(self, cost_action=False, discard=False)

    def hook_trash_this_card(self, game, player):
        if self.want_to_play(player):
            player.play_card(self, cost_action=False, discard=False)

    def want_to_play(self, player) -> bool:
        options = [("Don't use", False), ("Use Trail", True)]
        use_it = player.plr_choose_options(
            "Play Trail for +1 Card, +1 Action?", *options
        )
        return use_it


###############################################################################
class TestTrail(unittest.TestCase):
    """Test Trail"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Trail", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Trail")

    def test_play_card(self):
        """Play a card"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)  # One to play
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 1)

    def test_gain_card(self):
        """Gain a card"""
        self.plr.piles[Piles.HAND].empty()
        actions = self.plr.actions.get()
        self.plr.test_input = ["Use Trail"]
        self.plr.gain_card("Trail")
        self.assertEqual(self.plr.actions.get(), actions + 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 1)
        self.assertIn("Trail", self.plr.piles[Piles.PLAYED])

    def test_trash_card(self):
        """Trash self"""
        actions = self.plr.actions.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.test_input = ["Use Trail"]
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1)
        self.assertIn("Trail", self.g.trash_pile)

    def test_discard_card(self):
        """Discard self"""
        actions = self.plr.actions.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.phase = Phase.BUY
        self.plr.test_input = ["Use Trail"]
        self.plr.discard_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1)
        self.assertIn("Trail", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
