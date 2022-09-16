#!/usr/bin/env python

import unittest
import dominion.Card as Card
import dominion.Game as Game


###############################################################################
class Card_Fortune(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+1 Buy
        When you play this, double your Coin if you haven't yet this turn.
        When you gain this, gain a Gold per Gladiator you have in play."""
        self.name = "Fortune"
        self.buys = 1
        self.cost = 8
        self.debtcost = 8
        self.numcards = 5

    def special(self, game, player):
        if player.do_once("Fortune"):
            player.coins.set(player.coins.get() * 2)

    def hook_gain_this_card(self, game, player):
        num_gladiators = sum([1 for c in player.played if c.name == "Gladiator"])
        if num_gladiators:
            player.output("Gaining %d Gold" % num_gladiators)
            for _ in range(num_gladiators):
                player.gain_card("Gold")


###############################################################################
class Test_Fortune(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Fortune"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Fortune"].remove()

    def test_play(self):
        """Play a Fortune"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
