#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Zombie_Spy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ZOMBIE]
        self.base = Game.NOCTURNE
        self.desc = "+1 Card; +1 Action; Look at the top card of your deck. Discard it or put it back."
        self.name = "Zombie Spy"
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1
        self.cards = 1
        self.actions = 1

    def setup(self, game):
        game.trashpile.add(self)

    def special(self, game, player):
        c = player.nextCard()
        discard = player.plrChooseOptions(
            "Discard your card?",
            ("Keep %s on your deck" % c.name, False),
            ("Discard %s" % c.name, True),
        )
        if discard:
            player.addCard(c, "discard")
            player.output("Zombie Spy discarded your %s" % c.name)
        else:
            player.addCard(c, "topdeck")


###############################################################################
class Test_Zombie_Spy(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Zombie Spy"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Zombie Spy"].remove()

    def test_play_keep(self):
        self.plr.test_input = ["Keep"]
        self.plr.set_deck("Province", "Estate")
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertIsNotNone(self.plr.in_deck("Province"))

    def test_play_discard(self):
        self.plr.test_input = ["Discard"]
        self.plr.set_deck("Province", "Estate")
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertIsNone(self.plr.in_deck("Province"))
        self.assertIsNotNone(self.plr.in_discard("Province"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
