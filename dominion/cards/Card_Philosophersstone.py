#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Philosophersstone(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.ALCHEMY
        self.desc = "When you play this, count your deck and discard pile. Worth 1 Coin per 5 cards total between them (rounded down)"
        self.name = "Philosopher's Stone"
        self.cost = 3
        self.required_cards = ["Potion"]
        self.potcost = True

    def hook_coinvalue(self, game, player):
        """When you play this, count your deck and discard pile.
        Worth 1 per 5 cards total between them (rounded down)"""
        numcards = player.deck.size() + player.discardpile.size()
        extracoin = numcards / 5
        player.output("Gained %d coins from Philosopher's Stone" % extracoin)
        return int(extracoin)


###############################################################################
class Test_Philosophersstone(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Philosopher's Stone"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Philosopher's Stone"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a philosophers stone with not much on"""
        self.plr.set_deck("Estate")
        self.plr.set_discard("Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 0)

    def test_play_value(self):
        """Play a philosophers stone with the full Nicholas Flamel"""
        self.plr.set_deck("Estate", "Estate", "Estate", "Estate", "Silver")
        self.plr.set_discard("Estate", "Estate", "Estate", "Estate", "Silver")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
