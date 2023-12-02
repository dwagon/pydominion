#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, Phase, OptionKeys


###############################################################################
class Card_Spices(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Spices"
        self.coin = 2
        self.buys = 1
        self.cost = 5

    ###########################################################################
    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return "+2 Coin; +1 Buy; When you gain this, +2 Coffers."
        return "+2 Coin; +1 Buy"

    ###########################################################################
    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.coffers.add(2)
        return {}


###############################################################################
class TestSpices(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Spices"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self) -> None:
        self.card = self.g.get_card_from_pile("Spices")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.coffers.set(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1 + 1)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.coffers.get(), 0)

    def test_gain_card(self) -> None:
        self.plr.coffers.set(0)
        self.plr.gain_card("Spices")
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.coffers.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
