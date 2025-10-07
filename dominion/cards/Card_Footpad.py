#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Footpad"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys, Phase


###############################################################################
class Card_Footpad(Card.Card):
    """Footpad"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.CORNUCOPIA_GUILDS
        self.name = "Footpad"
        self.cost = 5
        self.desc = """+2 Coffers; Each other player discards down to 3 cards in hand."""

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        player.coffers.add(2)
        for plr in player.attack_victims():
            plr.output(f"{player}'s Footpad: Discard down to 3 cards")
            plr.plr_discard_down_to(3)

    def hook_any_gain_card(
        self, game: "Game.Game", player: "Player.Player", card: "Card.Card"
    ) -> dict[OptionKeys, Any]:
        """In games using this, when you gain a card in an Action phase, +1 Card"""
        if player.phase == Phase.ACTION:
            player.pickup_cards(1)
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    num_to_discard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(num_to_discard)


###############################################################################
class Test_Footpad(unittest.TestCase):
    """Test Footpad"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Footpad"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Footpad")
        self.plr.add_card(self.card, Piles.HAND)

    def test_attack(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.vic.test_input = ["1", "2", "0"]
        coffers = self.plr.coffers.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.piles[Piles.HAND].size(), 3)  # Normal  - 2
        self.assertEqual(self.vic.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.plr.coffers.get(), coffers + 2)

    def test_any_hook(self):
        self.plr.phase = Phase.ACTION
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.gain_card("Copper")
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
