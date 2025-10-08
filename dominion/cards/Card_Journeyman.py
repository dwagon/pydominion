#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Journeyman"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, NoCardException, Player


###############################################################################
class Card_Journeyman(Card.Card):
    """Journeyman"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = """Name a card.
            Reveal cards from the top of your deck until you reveal 3 cards that are not the named card.
            Put those cards into your hand and discard the rest."""
        self.name = "Journeyman"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        choices: list[tuple[str, Any]] = [("No guess", None)]
        for name, _ in sorted(game.get_card_piles()):
            choices.append((f"Guess {name}", name))
        opt = player.plr_choose_options(
            "Name a card. Reveal cards from your deck until you have 3 that aren't the named card", *choices
        )
        if not opt:
            return
        cards: list[Card.Card] = []
        max_cards = player.count_cards()
        count = max_cards
        while len(cards) < 3:
            try:
                card = player.next_card()
            except NoCardException:  # pragma: no coverage
                break
            player.reveal_card(card)
            if card.name == opt:
                player.output(f"Discarding {card}")
                player.discard_card(card)
            else:
                cards.append(card)
            count -= 1
            if count <= 0:  # pragma: no coverage
                player.output("Not enough suitable cards")
                break
        for card in cards:
            player.add_card(card, Piles.HAND)
            player.output(f"Pulling {card} into hand")


###############################################################################
class TestJourneyman(unittest.TestCase):
    """Test Journeyman"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Journeyman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Journeyman")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play the pawn - select card and action"""
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Duchy", "Province", "Gold")
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])

    def test_play_guess_none(self) -> None:
        """Chose not to guess"""
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Duchy", "Province", "Gold")
        self.plr.test_input = ["No guess"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Province", self.plr.piles[Piles.DECK])
        self.assertIn("Estate", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
