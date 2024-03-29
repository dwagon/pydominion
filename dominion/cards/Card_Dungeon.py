#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Dungeon"""
import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Dungeon(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Action. Now and next turn: +2 cards then discard 2 cards"
        self.name = "Dungeon"
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        self.sifter(game, player)

    def duration(self, game, player):
        self.sifter(game, player)

    def sifter(self, game, player):
        """+2 Cards, then discard 2 cards."""
        player.pickup_cards(2)
        player.plr_discard_cards(num=2, force=True)


###############################################################################
class Test_Dungeon(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Dungeon"], badcards=["Shaman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Dungeon")

    def test_playcard(self):
        """Play a dungeon"""
        self.plr.piles[Piles.DECK].set(
            "Estate", "Estate", "Estate", "Estate", "Estate", "Silver", "Gold"
        )
        self.plr.piles[Piles.HAND].set("Province", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["province", "duchy", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), 2
        )  # 2 picked up from dungeon -2 discard
        self.assertNotIn("duchy", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.plr.end_turn()
        self.plr.test_input = ["1", "2", "finish"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)
        self.assertEqual(self.plr.piles[Piles.PLAYED][-1].name, "Dungeon")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), 5
        )  # 5 dealt + 2 from dungeon -2 discard


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
