#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Haunted_Mirror(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.HEIRLOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Coin; When you trash this, you may discard an Action card, to gain a Ghost from its pile."
        self.name = "Haunted Mirror"
        self.cost = 0
        self.coin = 1
        self.required_cards = [("Card", "Ghost")]
        self.purchasable = False

    def hook_trashThisCard(self, game, player):
        ac = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not ac:
            player.output("No action cards in hand, no effect")
            return
        td = player.plr_discard_cards(cardsrc=ac)
        if td:
            player.gain_card("Ghost")


###############################################################################
class Test_Haunted_Mirror(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Cemetery", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Haunted Mirror"].remove()

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_trash_nothing(self):
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.trash_card(self.card)
        self.assertNotIn("Ghost", self.plr.piles[Piles.DISCARD])

    def test_trash(self):
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Moat"]
        self.plr.trash_card(self.card)
        self.assertIn("Ghost", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
