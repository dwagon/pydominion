#!/usr/bin/env python

import unittest
from dominion import Card, Game


##########################################################################
class Card_Pearldiver(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = "+1 card, +1 action. Put bottom of deck to top"
        self.name = "Pearl Diver"
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        """Look at the bottom card of your deck. You may put it on top"""
        if player.deck.size() == 0:
            player.refill_deck()
        bcard = player.deck[0]
        top = player.plr_choose_options(
            "What to do with bottom card?",
            ("Keep %s on bottom of deck" % bcard.name, False),
            ("Put %s on top of deck" % bcard.name, True),
        )
        if top:
            player.output("Putting %s on top of deck" % bcard.name)
            player.deck.remove(bcard)
            player.add_card(bcard, "topdeck")
        else:
            pass


###############################################################################
class Test_Pearldiver(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Pearl Diver"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.pearldiver = self.g["Pearl Diver"].remove()
        self.plr.add_card(self.pearldiver, "hand")

    def test_play(self):
        self.plr.deck.set("Copper", "Gold", "Province", "Silver", "Duchy")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.pearldiver)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_donothing(self):
        self.plr.deck.set("Copper", "Estate", "Gold", "Province", "Silver", "Duchy")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.pearldiver)
        self.assertEqual(self.plr.deck[-1].name, "Silver")
        self.assertEqual(self.plr.deck[0].name, "Copper")

    def test_putontop(self):
        self.plr.deck.set("Copper", "Estate", "Gold", "Province", "Silver", "Duchy")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.pearldiver)
        # Duchy gets pulled due to +1 card
        self.assertEqual(self.plr.deck[-1].name, "Copper")
        self.assertEqual(self.plr.deck[0].name, "Estate")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
