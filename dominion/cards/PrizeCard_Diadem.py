#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Diadem(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.PRIZE]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.name = "Diadem"
        self.purchasable = False
        self.cost = 0
        self.desc = "2 Coin. When you play this, +1 Coin per unused Action you have (Action, not Action card)."
        self.coin = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.output("Gaining %d coins from unused actions" % player.actions.get())
        player.coins.add(player.actions.get())


###############################################################################
class TestDiadem(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Tournament"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Diadem")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        self.plr.play_card(self.card)
        self.plr.actions.set(1)
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
