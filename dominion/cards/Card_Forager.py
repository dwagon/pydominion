#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles


###############################################################################
class Card_Forager(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Action +1 Buy;Trash a card from your hand. A coin per differently named Treasure in the trash."""
        self.name = "Forager"
        self.actions = 1
        self.buys = 1
        self.cost = 3

    ###########################################################################
    def special(self, game, player):
        player.plr_trash_card()
        treas = set()
        for card in game.trash_pile:
            if card.isTreasure():
                treas.add(card.name)
        player.coins.add(len(treas))
        player.output("Gained %s from Forager" % len(treas))


###############################################################################
class Test_Forager(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forager"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Forager")

    def test_play(self):
        """Play a forager"""
        self.plr.trash_card(self.g.get_card_from_pile("Copper"))
        self.plr.trash_card(self.g.get_card_from_pile("Silver"))
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertIn("Province", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
