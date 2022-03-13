#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Vagrant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 card, +1 action, Reveal the top card of your deck.
            If it's a Curse, Ruins, Shelter or Victory card, put it into your hand"""
        self.name = "Vagrant"
        self.actions = 1
        self.cards = 1
        self.cost = 2

    def special(self, game, player):
        """ " Reveal the top card of your deck. If it's a Curse,
        Ruins, Shelter or Victory card, put it into your hand"""
        c = player.next_card()
        player.reveal_card(c)
        if c.isVictory() or c.isRuin() or c.isShelter() or c.name == "Ruins":
            player.add_card(c, "hand")
            player.output("Adding %s to hand" % c.name)
        else:
            player.add_card(c, "topdeck")
            player.output("Top card %s still on deck" % c.name)


###############################################################################
class Test_Vagrant(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Vagrant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Vagrant"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the vagrant with unexciting next card"""
        self.plr.set_deck("Gold", "Silver", "Copper")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.next_card().name, "Silver")

    def test_play_exciting(self):
        """Play the vagrant with an exciting next card"""
        self.plr.set_deck("Estate", "Province", "Duchy")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertTrue(self.plr.in_hand("Province"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
