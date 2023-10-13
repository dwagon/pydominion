#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Cabin_Boy"""

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_CabinBoy(Card.Card):
    """Cabin Boy"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Card; +1 Action; At the start of your next turn, choose one: +$2;
        or trash this to gain a Duration card."""
        self.cards = 1
        self.actions = 1
        self.name = "Cabin Boy"
        self.cost = 4

    def duration(self, game, player):
        """choose one: +$2; or trash this to gain a Duration card."""
        options = [
            ("Gain $2", "money"),
            ("Trash this to gain a Duration card", "trash"),
        ]
        choice = player.plr_choose_options("What to do with Cabin Boy?", *options)
        match choice:
            case "money":
                player.coins.add(2)
            case "trash":
                player.trash_card(self)
                durations = []
                for name, pile in game.get_card_piles():
                    if game.card_instances[name].isDuration():
                        durations.append((f"Get {name}", name))
                which_duration = player.plr_choose_options(
                    "Which duration to gain?", *durations
                )
                player.gain_card(which_duration)


###############################################################################
class TestCabinBoy(unittest.TestCase):
    """Test Cabin Boy"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cabin Boy"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Cabin Boy")

    def test_gain_cash(self):
        """Play the card and gain cash"""
        self.plr.add_card(self.card, Piles.HAND)
        actions = self.plr.actions.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)  # -1 for playing CB
        self.assertEqual(
            len(self.plr.piles[Piles.HAND]), hand_size + 1 - 1
        )  # -1 for playing CB
        self.plr.end_turn()
        self.plr.test_input = ["Gain $2"]
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 2)

    def test_gain_duration(self):
        """Play the card and gain duration"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.test_input = ["Gain a duration", "Get Cabin Boy"]
        self.plr.start_turn()
        self.assertIn("Cabin Boy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Cabin Boy", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
