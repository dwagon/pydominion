#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Jester(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.CORNUCOPIA
        self.desc = """+2 Coin. Each other player discards the top card of his deck.
            If it's a Victory card he gains a Curse. Otherwise either he gains a
            copy of the discarded card or you do, your choice."""
        self.name = "Jester"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        for plr in player.attackVictims():
            card = plr.nextCard()
            plr.discardCard(card)
            plr.output("%s's Jester discarded your %s" % (player.name, card.name))
            if card.isVictory():
                plr.output("%s's Jester cursed you" % player.name)
                player.output("Cursed %s" % plr.name)
                plr.gainCard("Curse")
                continue
            getcard = player.plrChooseOptions(
                "Who should get a copy of %s's %s" % (plr.name, card.name),
                ("You get a %s" % card.name, True),
                ("%s gets a %s" % (plr.name, card.name), False),
            )
            if getcard:
                player.gainCard(card.name)
            else:
                plr.output("%s's Jester gave you a %s" % (player.name, card.name))
                plr.gainCard(card.name)


###############################################################################
class Test_Jester(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Jester"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Jester"].remove()
        self.plr.addCard(self.card, "hand")

    def test_victory(self):
        """Play a jester with the victim having a Victory on top of deck"""
        self.victim.setDeck("Duchy")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.victim.in_discard("Curse"))
        self.assertIsNotNone(self.victim.in_discard("Duchy"))

    def test_give_card(self):
        """Play a jester and give the duplicate to the victim"""
        self.victim.setDeck("Gold")
        self.plr.test_input = ["gets"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.victim.discardpile.size(), 2)
        self.assertEqual(self.plr.discardpile.size(), 0)
        for c in self.victim.discardpile:
            self.assertEqual(c.name, "Gold")
        self.assertIsNone(self.victim.in_discard("Curse"))
        self.assertIsNotNone(self.victim.in_discard("Gold"))
        self.assertIsNone(self.plr.in_discard("Gold"))

    def test_take_card(self):
        """Play a jester and take the duplicate from the victim"""
        self.victim.setDeck("Gold")
        self.plr.test_input = ["you"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.victim.discardpile.size(), 1)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertIsNone(self.victim.in_discard("Curse"))
        self.assertIsNotNone(self.victim.in_discard("Gold"))
        self.assertIsNotNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
