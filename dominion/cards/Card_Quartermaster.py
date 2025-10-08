#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Quartermaster"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys, PlayArea

QM = "quartermaster"


###############################################################################
class Card_Quartermaster(Card.Card):
    """Quartermaster"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """At the start of each of your turns for the rest of the game,
            choose one: Gain a card costing up to $4, setting it aside on this;
            or put a card from this into your hand."""
        self.name = "Quartermaster"
        self.cost = 5
        self.permanent = True

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        """At the start of each of your turns for the rest of the game, choose one: Gain a card costing up to $4,
        setting it aside on this; or put a card from this into your hand."""
        if QM not in player.specials:
            player.specials[QM] = PlayArea.PlayArea("Quartermaster")
        if self not in player.end_of_game_cards:
            player.end_of_game_cards.append(self)
        options: list[tuple[str, Any]] = [("Gain a card costing up to $4", None)]
        for card in player.specials[QM]:
            options.append((f"Put {card} back into your hand", card))

        choice = player.plr_choose_options("What to do with Quartermaster?", *options)
        if choice is None:
            if card := player.plr_gain_card(cost=4):
                player.move_card(card, player.specials[QM])
                player.secret_count += 1
        else:
            player.specials[QM].remove(choice)
            player.add_card(choice, Piles.HAND)
            player.secret_count -= 1

        return {}

    def hook_end_of_game(self, game: Game.Game, player: Player.Player) -> None:
        """So any victory cards are counted at the end"""
        for card in player.specials[QM]:
            player.add_card(card, Piles.HAND)


###############################################################################
class TestQuartermaster(unittest.TestCase):
    """Test Quartermaster"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Quartermaster", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Quartermaster")

    def test_play_card(self) -> None:
        """Play a Quartermaster"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.test_input = ["Gain a card", "Get Moat"]
        self.plr.start_turn()
        self.assertNotIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Moat", self.plr.specials[QM])
        self.assertIn("Quartermaster", self.plr.piles[Piles.DURATION])
        self.plr.end_turn()
        self.plr.test_input = ["Put Moat"]
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertNotIn("Moat", self.plr.specials[QM])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
