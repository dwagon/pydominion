#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player, Piles


###############################################################################
class Card_Mountebank(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+2 coin. Each other player may discard a Curse. If he doesn't, he gains a Curse and a Copper."
        self.name = "Mountebank"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        for plr in player.attack_victims():
            for c in plr.piles[Piles.HAND]:
                if c.name == "Curse":
                    player.output("Player %s discarded a curse" % plr.name)
                    plr.output("Discarded a Curse due to %s's Mountebank" % player.name)
                    plr.discard_card(c)
                    break
            else:
                player.output("Player %s gained a curse and a copper" % plr.name)
                plr.output("Gained a Curse and Copper due to %s's Mountebank" % player.name)
                plr.add_card(game["Curse"].remove())
                plr.add_card(game["Copper"].remove())


###############################################################################
class Test_Mountebank(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Mountebank"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.mountebank = self.g["Mountebank"].remove()
        self.curse = self.g["Curse"].remove()

    def test_hascurse(self):
        self.attacker.add_card(self.mountebank, Piles.HAND)
        self.victim.add_card(self.curse, Piles.HAND)
        self.attacker.play_card(self.mountebank)
        self.assertEqual(self.victim.piles[Piles.DISCARD][0].name, "Curse")

    def test_nocurse(self):
        self.attacker.add_card(self.mountebank, Piles.HAND)
        self.attacker.play_card(self.mountebank)
        discards = [c.name for c in self.victim.piles[Piles.DISCARD]]
        self.assertEqual(sorted(discards), sorted(["Curse", "Copper"]))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
