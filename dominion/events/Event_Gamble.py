#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Gamble """

import unittest
from dominion import Card, Game, Piles, Event, NoCardException


###############################################################################
class Event_Gamble(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+1 Buy; Reveal the top card of your deck. If it's a Treasure
            or Action, you may play it. Otherwise, discard it."""
        self.name = "Gamble"
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        """Reveal the top card of your deck. If it's a Treasure
        or Action, you may play it. Otherwise, discard it."""
        try:
            nxt = player.next_card()
        except NoCardException:
            return
        player.output(f"Next card is {nxt}")
        if nxt.isAction() or nxt.isTreasure():
            player.card_benefits(nxt)
        else:
            player.output("Card isn't a Treasure or Action - discarding")
        player.discard_card(nxt)


###############################################################################
class Test_Gamble(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Gamble"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Gamble"]

    def test_play_treasure(self):
        """Perform a Gamble with a treasure"""
        self.plr.coins.add(2)
        self.plr.piles[Piles.DECK].set("Gold")
        self.assertEqual(self.plr.buys.get(), 1)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertEqual(self.plr.buys.get(), 1)

    def test_play_action(self):
        """Perform a Gamble with an action"""
        self.plr.coins.add(2)
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Copper", "Moat")
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Moat"])
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertEqual(self.plr.buys.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
