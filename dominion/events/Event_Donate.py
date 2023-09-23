#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Donate(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """After this turn, put all cards from your deck and discard
            pile into your hand, trash any number, shuffle your hand into your
            deck, then draw 5 cards."""
        self.name = "Donate"
        self.cost = 0
        self.debtcost = 8

    def hook_end_turn(self, game, player):
        for area in (player.piles[Piles.HAND], player.piles[Piles.DECK], player.piles[Piles.PLAYED], player.piles[Piles.DISCARD]):
            for card in area:
                player.add_card(card, Piles.HAND)
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
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Gold", "Estate", "Copper", "Copper")
        self.plr.piles[Piles.DISCARD].set("Province", "Estate", "Copper", "Copper")
        self.plr.piles[Piles.DECK].set("Silver", "Estate", "Copper", "Copper")
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.debt.get(), 8)
        self.plr.test_input = ["Gold", "Province", "Silver", "finish"]
        self.plr.end_turn()
        self.g.print_state()
        self.assertIn("Gold", self.g.trash_pile)
        self.assertIn("Province", self.g.trash_pile)
        self.assertIn("Silver", self.g.trash_pile)
        self.assertNotIn("Gold", self.plr.piles[Piles.DECK])
        self.assertEqual(self.g.trash_pile.size(), tsize + 3)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
