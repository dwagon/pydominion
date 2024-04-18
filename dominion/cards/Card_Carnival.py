#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Carnival"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Carnival(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA_GUILDS
        self.name = "Carnival"
        self.cost = 5
        self.desc = """Reveal the top 4 cards of your deck.
        Put one of each differently named card into your hand and discard the rest."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        card_names: list[str] = []
        for _ in range(4):
            try:
                card = player.next_card()
            except NoCardException:  # pragma: no cover
                break
            player.reveal_card(card)
            if card.name in card_names:
                player.discard_card(card)
                player.output(f"Discarding {card}")
            else:
                player.add_card(card, Piles.HAND)
                card_names.append(card.name)
                player.output(f"Adding {card} to hand")


###############################################################################
class Test_Carnival(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Carnival"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Carnival")

    def test_play(self) -> None:
        """Play a Carnival"""
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DISCARD].set()
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
