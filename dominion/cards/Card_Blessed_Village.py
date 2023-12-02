#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, OptionKeys, Phase


###############################################################################
class Card_BlessedVillage(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Blessed Village"
        self.actions = 2
        self.cards = 1
        self.cost = 4

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return """+1 Card; +2 Actions; When you gain this, take a Boon.
                Receive it now or at the start of your next turn."""
        return "+1 Card; +2 Actions"

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.receive_boon()
        return {}


###############################################################################
class Test_BlessedVillage(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, initcards=["Blessed Village"], badcards=["Druid"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Blessed Village")
        for b in self.g.boons:
            if b.name == "The Sea's Gift":
                self.g.boons = [b]
                break

    def test_play_card(self) -> None:
        """Play Blessed Village"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertGreaterEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_gain(self) -> None:
        self.plr.gain_card("Blessed Village")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)  # 1 from boon


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
