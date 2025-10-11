#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Sailor"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


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

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        """Once this turn, when you gain a Duration card, you may play it."""
        if not card.isDuration() or player.has_done_once(self.uuid):
            return {}
        if player.plr_choose_options(
            f"Sailor lets you play {card} now",
            ("Don't play", False),
            ("Play now", True),
        ):
            player.do_once(self.uuid)
            player.output(f"Playing {card} from Sailor effect")
            player.play_card(card, cost_action=False, discard=False)
            return {OptionKeys.DESTINATION: Piles.DURATION}
        return {}

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        """At the start of your next turn, +$2; and you may trash a card from your hand."""
        player.coins.add(2)
        player.plr_trash_card(num=1)
        return {}


###############################################################################
class TestSailor(unittest.TestCase):
    """Test Sailor"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sailor", "Raider"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sailor")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play a sailor"""
        self.plr.play_card(self.card)
        self.plr.test_input = ["Play now"]
        num_raiders = len(self.g.card_piles["Raider"])
        self.plr.gain_card("Raider")
        self.g.print_state(True)
        self.assertIn("Raider", self.plr.piles[Piles.DURATION])
        self.assertIn("Sailor", self.plr.piles[Piles.DURATION])
        self.assertEqual(len(self.g.card_piles["Raider"]), num_raiders - 1)
        self.plr.end_turn()
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper")
        self.plr.test_input = ["Trash Copper"]
        self.plr.start_turn()
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper")
        self.plr.piles[Piles.DECK].set("Province")
        self.assertEqual(self.plr.coins.get(), 2 + 3)  # 2 for sailor, 3 for Raider
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Raider", self.plr.piles[Piles.PLAYED])
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
