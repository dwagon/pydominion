#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Sauna"""
import unittest
from typing import Optional

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Sauna(Card.Card):
    """Sauna"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROMO
        self.desc = """+1 Card; +1 Action; You may play an Avanto from your hand. 
        This turn, when you play a Silver, you may trash a card from your hand."""
        self.name = "Sauna"
        self.cost = 4
        self.cards = 1
        self.actions = 1
        self.numcards = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may play an Avanto from your hand."""
        if avanto := player.piles[Piles.HAND]["Avanto"]:
            if player.plr_choose_options(
                "Play an Avanto from your hand",
                ("Play Avanto", True),
                ("Don't play", False),
            ):
                player.play_card(avanto, cost_action=False)

    def hook_post_play(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, str]:
        """This turn, when you play a Silver, you may trash a card from your hand."""
        if card.name != "Silver":
            return {}
        player.output("Sauna lets you trash a card")
        player.plr_trash_card(num=1)
        return {}


###############################################################################
class TestSauna(unittest.TestCase):
    """Test Sauna"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sauna"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sauna")

    def test_play_not_have(self) -> None:
        """Play a Sauna - without having an Avanto"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate")
        hand_size = len(self.plr.piles[Piles.HAND])
        actions = self.plr.actions.get()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1)
        self.assertEqual(self.plr.actions.get(), actions)  # +1, -1

    def test_play_has(self) -> None:
        """Play a Sauna - having an Avanto"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate", "Avanto")
        hand_size = len(self.plr.piles[Piles.HAND])
        actions = self.plr.actions.get()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Play Avanto"]
        self.plr.play_card(self.card)
        self.assertEqual(
            len(self.plr.piles[Piles.HAND]), hand_size + 1 + 3 - 1
        )  # +1 for Sauna, +3 for Avanto, -1 for playing Avanto
        self.assertEqual(self.plr.actions.get(), actions)  # +1, -1
        self.assertIn("Avanto", self.plr.piles[Piles.PLAYED])

    def test_play_silver(self) -> None:
        """Play a Silver"""
        self.plr.piles[Piles.HAND].set("Sauna", "Estate", "Duchy")
        silver = self.g.get_card_from_pile("Silver")
        self.plr.add_card(silver, Piles.HAND)
        self.plr.test_input = ["Trash Duchy"]
        self.plr.play_card(silver)
        self.assertIn("Duchy", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
