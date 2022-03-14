#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Donate(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = """After this turn, put all cards from your deck and discard
            pile into your hand, trash any number, shuffle your hand into your
            deck, then draw 5 cards."""
        self.name = "Donate"
        self.cost = 0
        self.debtcost = 8

    def hook_end_turn(self, game, player):
        for area in (player.hand, player.deck, player.played, player.discardpile):
            for card in area[:]:
                player.add_card(card, "hand")
                area.remove(card)
        player.plr_trash_card(anynum=True, prompt="Donate allows you to trash any cards")
        player.discard_hand()
        player.pickup_cards(5)


###############################################################################
class Test_Donate(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=["Donate"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Donate"]

    def test_with_treasure(self):
        """Use Donate"""
        tsize = self.g.trashSize()
        self.plr.set_hand("Gold", "Estate", "Copper", "Copper")
        self.plr.set_discard("Province", "Estate", "Copper", "Copper")
        self.plr.set_deck("Silver", "Estate", "Copper", "Copper")
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.debt, 8)
        self.plr.test_input = ["Gold", "Province", "Silver", "finish"]
        self.plr.end_turn()
        self.g.print_state()
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertIsNotNone(self.g.in_trash("Province"))
        self.assertIsNotNone(self.g.in_trash("Silver"))
        self.assertIsNone(self.plr.in_deck("Gold"))
        self.assertEqual(self.g.trashSize(), tsize + 3)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.discardpile.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
