#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Abundance """
import unittest
from typing import Optional, Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Abundance(Card.Card):
    """Abundance"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """The next time you gain an Action card: +1 Buy and +$3."""
        self.name = "Abundance"
        self.cost = 4
        self.permanent = True

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> Optional[dict[OptionKeys, Any]]:
        """+1 Buy and +$3."""
        if card.isAction():
            player.output(f"Abundance triggered due to gaining {card}")
            player.buys.add(1)
            player.coins.add(3)
            player.move_card(self, Piles.DISCARD)
        return None


###############################################################################
class TestAbundance(unittest.TestCase):
    """Test Abundance"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Abundance", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Abundance")

    def test_gain_action(self) -> None:
        """Play an Abundance"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(self.plr.coins.get(), coins + 3)
        self.assertIn("Abundance", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
