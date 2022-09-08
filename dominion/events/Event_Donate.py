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
            for card in area:
                player.add_card(card, "hand")
                area.remove(card)
        player.plr_trash_card(anynum=True, prompt="Donate allows you to trash any cards")
        player.discard_hand()
        player.pickup_cards(5)


###############################################################################
class Test_Donate(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Donate"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Donate"]

    def test_with_treasure(self):
        """Use Donate"""
        tsize = self.g.trashpile.size()
        self.plr.hand.set("Gold", "Estate", "Copper", "Copper")
        self.plr.discardpile.set("Province", "Estate", "Copper", "Copper")
        self.plr.deck.set("Silver", "Estate", "Copper", "Copper")
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.debt, 8)
        self.plr.test_input = ["Gold", "Province", "Silver", "finish"]
        self.plr.end_turn()
        self.g.print_state()
        self.assertIn("Gold", self.g.trashpile)
        self.assertIn("Province", self.g.trashpile)
        self.assertIn("Silver", self.g.trashpile)
        self.assertNotIn("Gold", self.plr.deck)
        self.assertEqual(self.g.trashpile.size(), tsize + 3)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.discardpile.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
