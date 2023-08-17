#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Bonfire(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Trash up to two cards you have in play"
        self.name = "Bonfire"
        self.cost = 3

    def special(self, game, player):
        """Trash up to two cards you have in play"""
        player.plr_trash_card(num=2, cardsrc="played")


###############################################################################
class Test_Bonfire(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Bonfire"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Bonfire"]
        self.copper = self.g["Copper"].remove()
        self.gold = self.g["Gold"].remove()
        self.estate = self.g["Estate"].remove()

    def test_bonfire(self):
        """Use Bonfire"""
        tsize = self.g.trashpile.size()
        self.plr.coins.add(3)
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.add_card(self.copper, Piles.HAND)
        self.plr.play_card(self.copper)
        self.plr.add_card(self.gold, Piles.HAND)
        self.plr.play_card(self.gold)
        self.plr.test_input = ["Copper", "Gold", "Finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.g.trashpile.size(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
