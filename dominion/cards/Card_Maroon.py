#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Maroon"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Maroon(Card.Card):
    """Secluded Shrine"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Trash a card from your hand. +2 Cards per type it has (Action, Attack, etc.)."""
        self.name = "Maroon"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may trash a card from your hand."""
        cards = player.plr_trash_card(num=1, printtypes=True)
        if not cards:
            return
        if isinstance(cards[0].cardtype, list):
            num_types = len(cards[0].cardtype)
        else:
            num_types = 1
        player.output(f"Picking up {num_types *2} cards")
        player.pickup_cards(num=num_types * 2)


###############################################################################
class TestMaroon(unittest.TestCase):
    """Test Maroon"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Maroon", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Maroon")

    def test_play(self) -> None:
        """Play a Maroon"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)

        self.plr.test_input = ["Trash Moat"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIn("Moat", self.g.trash_pile)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
