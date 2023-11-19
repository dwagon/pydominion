#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sailor"""

import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Sailor(Card.Card):
    """Sailor"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+1 Action; Once this turn, when you gain a Duration card, you may play it.
            At the start of your next turn, +$2 and you may trash a card from your hand."""
        self.actions = 1
        self.name = "Sailor"
        self.cost = 4

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> Optional[dict[str, Any]]:
        """Once this turn, when you gain a Duration card, you may play it."""
        if not card.isDuration():
            return {}
        if player.do_once("Sailor"):
            if to_play := player.plr_choose_options(
                f"Sailor lets you play {card} now",
                ("Don't play", False),
                ("Play now", True),
            ):
                player.move_card(card, Piles.HAND)
                player.output(f"Playing {card} from Sailor effect")
                player.play_card(card, cost_action=False)
                return {"dontadd": True}
        return {}

    def duration(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[str, Any]]:
        """At the start of your next turn, +$2; and you may trash a card from your hand."""
        player.coins.add(2)
        player.plr_trash_card(num=1)
        return None


###############################################################################
class Test_Sailor(unittest.TestCase):
    """Test Sailor"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sailor", "Guardian"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sailor")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a sailor"""
        self.plr.play_card(self.card)
        self.plr.test_input = ["Play now"]
        self.plr.gain_card("Guardian")
        self.assertIn("Guardian", self.plr.piles[Piles.DURATION])
        self.assertIn("Sailor", self.plr.piles[Piles.DURATION])
        self.plr.end_turn()
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper")
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.test_input = ["Trash Copper"]
        self.plr.start_turn()
        self.g.print_state()
        self.assertEqual(self.plr.coins.get(), 3)  # 2 for sailor, 1 for guardian
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Guardian", self.plr.piles[Piles.PLAYED])
        self.assertIn("Sailor", self.plr.piles[Piles.PLAYED])

    def test_play_no_duration(self) -> None:
        """Play a sailor but don't gain a duration card"""
        self.plr.play_card(self.card)
        self.plr.test_input = ["Play now"]
        self.plr.gain_card("Province")
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper")
        self.plr.test_input = ["Trash Copper"]
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
