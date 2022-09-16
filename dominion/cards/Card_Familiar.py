#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Familiar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "+1 card, +1 action; Each other player gains a Curse."
        self.name = "Familiar"
        self.cards = 1
        self.actions = 1
        self.cost = 3
        self.required_cards = ["Potion", "Curse"]
        self.potcost = True

    def special(self, game, player):
        """All other players gain a curse"""
        for pl in player.attack_victims():
            player.output("%s got cursed" % pl.name)
            pl.output("%s's Familiar cursed you" % player.name)
            pl.gain_card("Curse")


###############################################################################
class Test_Familiar(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Familiar", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Familiar"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a familiar"""
        self.plr.play_card(self.card)
        self.assertEqual(self.victim.discardpile[0].name, "Curse")
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 1)

    def test_defended(self):
        self.victim.hand.set("Gold", "Moat")
        self.plr.play_card(self.card)
        self.assertTrue(self.victim.discardpile.is_empty())
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
