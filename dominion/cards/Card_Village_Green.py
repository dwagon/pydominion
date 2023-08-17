#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Village_Green """

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Village_Green(Card.Card):
    """Village Green"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.REACTION,
        ]
        self.cost = 4
        self.name = "Village Green"
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Either now or at the start of your next turn, +1 Card and +2 Actions.
            When you discard this other than during Clean-up, you may reveal it to play it."""
        self._choice = "undef"

    def special(self, game, player):
        """Either now or at the start of your next turn, +1 Card and +2 Actions."""
        choice = player.plr_choose_options(
            "Pick One",
            ("Now: +1 Cards and +2 Actions", "now"),
            ("or Next Turn: +1 Cards and +2 Actions", "then"),
        )
        if choice == "now":
            player.pickup_cards(1)
            player.add_actions(2)
            self._choice = "now"
        else:
            self._choice = "then"

    def duration(self, game, player):
        """Now or then"""
        if self._choice == "then":
            player.pickup_cards(1)
            player.add_actions(2)
        self._choice = "undef"

    def hook_discard_this_card(self, game, player, source):
        """When you discard this other than during Clean-up, you may reveal it to play it."""
        if player.phase == Player.Phase.CLEANUP:
            return
        play = player.plr_choose_options(
            "Reveal this card to play it?",
            ("Reveal and play", True),
            ("Keep concealed", False),
        )
        if play:
            player.move_card(self, Piles.HAND)
            player.play_card(self)


###############################################################################
class Test_Village_Green(unittest.TestCase):
    """Test Village Green"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Village Green", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Village Green"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_this_turn(self):
        """Play Card with effect this turn"""
        self.plr.test_input = ["Now"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)

    def test_play_next_turn(self):
        """Play Card with effect next turn"""
        self.plr.test_input = ["Next"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.actions.get(), 2 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)

    def test_discard(self):
        """Discard when not cleanup"""
        self.plr.piles[Piles.DECK].set("Duchy")
        self.plr.phase = Player.Phase.BUY
        self.plr.test_input = ["Reveal", "Now"]
        self.plr.discard_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertIn("Village Green", self.plr.piles[Piles.DURATION])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
