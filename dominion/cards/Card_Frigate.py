#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Frigate"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Frigate(Card.Card):
    """Secluded Shrine"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+$3; Until the start of your next turn, each time another player plays an Action card,
        they discard down to 4 cards in hand afterwards."""
        self.name = "Frigate"
        self.cost = 5
        self.coin = 3

    def hook_all_players_post_play(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> dict[OptionKeys, Any]:
        """each time another player plays an Action card, they discard down to 4 cards in hand afterwards."""
        if player != owner:
            player.output(f"{owner.name}'s Frigate: Discard down to 4 cards")
            player.plr_discard_down_to(4)
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    num_to_discard = len(player.piles[Piles.HAND]) - 4
    return player.pick_to_discard(num_to_discard)


###############################################################################
class TestFrigate(unittest.TestCase):
    """Test Frigate"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Frigate", "Village"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Frigate")

    def test_play(self) -> None:
        """Play a Frigate"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 3)

    def test_attack(self) -> None:
        """Another player plays action"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        village = self.g.get_card_from_pile("Village")
        self.victim.add_card(village, Piles.HAND)
        self.victim.test_input = ["1", "2", "0"]
        self.victim.play_card(village)
        self.assertEqual(len(self.victim.piles[Piles.HAND]), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
