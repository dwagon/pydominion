#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Followers(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_PRIZE]
        self.base = Game.CORNUCOPIA
        self.name = "Followers"
        self.purchasable = False
        self.required_cards = ["Curse"]
        self.cost = 0
        self.desc = "+2 Cards. Gain an Estate. Each other player gains a Curse and discards down to 3 cards in hand."
        self.cards = 2

    def special(self, game, player):
        player.gainCard("Estate")
        for plr in player.attackVictims():
            plr.output("%s's Followers cursed you" % player.name)
            plr.gainCard("Curse")
            plr.plrDiscardDownTo(3)


###############################################################################
class Test_Followers(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Tournament"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Followers"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        self.victim.set_hand("Copper", "Copper", "Copper", "Silver", "Gold")
        self.victim.test_input = ["silver", "gold", "finish"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2)
        self.assertEqual(self.victim.hand.size(), 3)
        self.assertIsNotNone(self.plr.in_discard("Estate"))
        self.assertIsNotNone(self.victim.in_discard("Curse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
