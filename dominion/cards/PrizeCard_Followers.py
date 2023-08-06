#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Followers(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.PRIZE,
        ]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.name = "Followers"
        self.purchasable = False
        self.required_cards = ["Curse"]
        self.cost = 0
        self.desc = "+2 Cards. Gain an Estate. Each other player gains a Curse and discards down to 3 cards in hand."
        self.cards = 2

    def special(self, game, player):
        player.gain_card("Estate")
        for plr in player.attack_victims():
            plr.output("%s's Followers cursed you" % player.name)
            plr.gain_card("Curse")
            plr.plr_discard_down_to(3)


###############################################################################
class Test_Followers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Tournament"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Followers"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.victim.hand.set("Copper", "Copper", "Copper", "Silver", "Gold")
        self.victim.test_input = ["silver", "gold", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2)
        self.assertEqual(self.victim.hand.size(), 3)
        self.assertIn("Estate", self.plr.discardpile)
        self.assertIn("Curse", self.victim.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
