#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Harbinger"""
import unittest
from typing import Any

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_Harbinger(Card.Card):
    """Harbinger"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+1 Card; +1 Action; Look through your discard pile. You may put a card from it onto your deck."
        self.name = "Harbinger"
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        choices: list[tuple[str, Any]] = [("Don't look through discard pile", None)]
        already = set()
        for card in player.piles[Piles.DISCARD]:
            if card.name in already:
                continue
            choices.append((f"Put {card} back in your deck", card))
            already.add(card.name)
        if not already:
            player.output("No suitable cards")
        player.output("Look through your discard pile. You may put a card from it onto your deck.")

        if choice := player.plr_choose_options("Which Card? ", *choices):
            player.add_card(choice, Piles.TOPDECK)
            player.piles[Piles.DISCARD].remove(choice)


###############################################################################
class TestHarbinger(unittest.TestCase):
    """Test Harbinger"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Harbinger"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Harbinger")

    def test_play(self):
        """Play a harbinger"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Province")
        self.plr.test_input = ["Put Gold"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
