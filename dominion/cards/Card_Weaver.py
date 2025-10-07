#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Weaver"""

import unittest

from dominion import Game, Card, Piles, Phase, Player, NoCardException, PlayArea


###############################################################################
class Card_Weaver(Card.Card):
    """Weaver"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Gain two Silvers or a card costing up to $4.
            When you discard this other than in Clean-up, you may play it."""
        self.name = "Weaver"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Gain 2 silvers or a $4 card"""
        if player.plr_choose_options(
            "Pick one:",
            ("Gain two silver", True),
            ("Gain a card costing up to $4", False),
        ):
            try:
                player.gain_card("Silver")
                player.gain_card("Silver")
            except NoCardException:
                player.output("No more Silver")
        else:
            player.plr_gain_card(4)

    def hook_discard_this_card(self, game: Game.Game, player: Player.Player, source: PlayArea.PlayArea) -> None:
        if player.phase != Phase.CLEANUP:
            player.play_card(self, cost_action=False, discard=False)


###############################################################################
class TestWeaver(unittest.TestCase):
    """Test Weaver"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Weaver", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Weaver")

    def test_play_gain_silver(self) -> None:
        """Play a Weaver to gain two silvers"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 2)

    def test_play_gain_cards(self) -> None:
        """Play a Weaver and gain cards"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gain a card", "Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])

    def test_play_non_cleanup(self) -> None:
        """Discard weaver not during cleanup"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gain a card", "Get Moat"]
        self.plr.phase = Phase.BUY
        self.plr.discard_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
