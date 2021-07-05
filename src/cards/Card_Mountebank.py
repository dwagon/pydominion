#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Mountebank(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.PROSPERITY
        self.desc = "+2 coin. Each other player may discard a Curse. If he doesn't, he gains a Curse and a Copper."
        self.name = "Mountebank"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        for plr in player.attackVictims():
            for c in plr.hand:
                if c.name == "Curse":
                    player.output("Player %s discarded a curse" % plr.name)
                    plr.output("Discarded a Curse due to %s's Mountebank" % player.name)
                    plr.discardCard(c)
                    break
            else:
                player.output("Player %s gained a curse and a copper" % plr.name)
                plr.output(
                    "Gained a Curse and Copper due to %s's Mountebank" % player.name
                )
                plr.addCard(game["Curse"].remove())
                plr.addCard(game["Copper"].remove())


###############################################################################
class Test_Mountebank(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Mountebank"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.mountebank = self.g["Mountebank"].remove()
        self.curse = self.g["Curse"].remove()

    def test_hascurse(self):
        self.attacker.addCard(self.mountebank, "hand")
        self.victim.addCard(self.curse, "hand")
        self.attacker.playCard(self.mountebank)
        self.assertEqual(self.victim.discardpile[0].name, "Curse")

    def test_nocurse(self):
        self.attacker.addCard(self.mountebank, "hand")
        self.attacker.playCard(self.mountebank)
        discards = [c.name for c in self.victim.discardpile]
        self.assertEqual(sorted(discards), sorted(["Curse", "Copper"]))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
