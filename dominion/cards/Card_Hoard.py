#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Hoard"""
import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Hoard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = (
            "+2 coin; While this is in play, when you buy a Victory card, gain a Gold"
        )
        self.name = "Hoard"
        self.playable = False
        self.coin = 2
        self.cost = 6

    def hook_buy_card(self, game, player, card):
        """When this is in play, when you buy a Victory card, gain a Gold"""
        if card.isVictory():
            player.output("Gaining Gold from Hoard")
            gold = game.get_card_from_pile("Gold")
            player.add_card(gold)


###############################################################################
class TestHoard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hoard"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Hoard")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())

    def test_buy_victory(self):
        self.plr.play_card(self.card)
        self.plr.buy_card("Estate")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for c in self.plr.piles[Piles.DISCARD]:
            if c.name == "Gold":
                break
        else:  # pragma: no cover
            self.fail("Didn't pickup gold")

    def test_buy_non_victory(self):
        self.plr.play_card(self.card)
        self.plr.buy_card("Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
