#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Poorhouse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DARKAGES
        self.desc = """+4 Coin. Reveal your hand. -1 Coin per Treasure card in your hand, to a minimum of 0."""
        self.name = "Poor House"
        self.cost = 1

    def special(self, game, player):
        coins = 4
        for card in player.hand:
            player.reveal_card(card)
            if card.isTreasure():
                coins -= 1
        player.output("Gaining %d coins" % max(coins, 0))
        player.addCoin(max(coins, 0))


###############################################################################
class Test_Poorhouse(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Poor House"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Poor House"].remove()

    def test_play(self):
        """Play an Poor House"""
        self.plr.set_hand("Estate", "Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 4 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
