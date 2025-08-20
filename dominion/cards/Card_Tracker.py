#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Tracker"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_Tracker(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Coin. This turn, when you gain a card, you may put it onto your deck. Receive a Boon."
        self.name = "Tracker"
        self.cost = 2
        self.coin = 1
        self.heirloom = "Pouch"

    def special(self, game, player) -> None:
        # Special flag to stop boon interfering with tests
        if not hasattr(player, "_tracker_dont_boon"):
            player.receive_boon()

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        """While this is in play, when you gain a card, you may
        put that card on top of your deck"""
        mod = {}
        if player.plr_choose_options(
            f"Where to put {card}?",
            (f"Put {card} on discard", False),
            (f"Put {card} on top of deck", True),
        ):
            player.output(f"Putting {card} on deck due to Tracker")
            mod[OptionKeys.DESTINATION] = "topdeck"
        return mod


###############################################################################
class TestTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Tracker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.plr._tracker_dont_boon = True  # type: ignore
        self.card = self.g.get_card_from_pile("Tracker")

    def test_play(self) -> None:
        """Play a Tracker"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.coins.get(), 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_discard(self) -> None:
        """Have a Tracker  - discard the gained card"""
        self.plr.piles[Piles.PLAYED].set("Tracker")
        self.plr.test_input = ["discard"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])

    def test_deck(self) -> None:
        """Have a Tracker  - the gained card on the deck"""
        self.plr.piles[Piles.PLAYED].set("Tracker")
        self.plr.test_input = ["deck"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
