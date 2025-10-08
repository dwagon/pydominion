#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Skirmisher(Card.Card):
    """Skirmisher"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Skirmisher"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.desc = """+1 Card; +1 Action; +$1; This turn, when you gain an
            Attack card, each other player discards down to 3 cards in hand."""
        self.cost = 5

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if not card.isAttack():
            return {}
        for plr in player.attack_victims():
            plr.output(f"{player}'s Skirmisher: Discard down to 3 cards")
            plr.plr_discard_down_to(3)
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class TestSkirmisher(unittest.TestCase):
    """Test Skirmisher"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Skirmisher"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Skirmisher")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_gain_plain(self) -> None:
        """Gain a non-attack card after this is in play"""
        self.plr.play_card(self.card)
        self.plr.gain_card("Silver")
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 5)

    def test_gain_attack(self) -> None:
        """Gain an attack card after this is in play"""
        self.victim.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.victim.test_input = ["Estate", "Duchy", "finish"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Skirmisher")
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
