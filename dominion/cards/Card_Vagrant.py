#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Vagrant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
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
            player.add_card(c, Piles.HAND)
            player.output("Adding %s to hand" % c.name)
        else:
            player.add_card(c, "topdeck")
            player.output("Top card %s still on deck" % c.name)


###############################################################################
class Test_Vagrant(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Vagrant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Vagrant"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the vagrant with unexciting next card"""
        self.plr.piles[Piles.DECK].set("Gold", "Silver", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.next_card().name, "Silver")

    def test_play_exciting(self):
        """Play the vagrant with an exciting next card"""
        self.plr.piles[Piles.DECK].set("Estate", "Province", "Duchy")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertIn("Province", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
