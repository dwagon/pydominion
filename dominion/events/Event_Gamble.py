#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Gamble """

import unittest
from dominion import Game, Event


###############################################################################
class Event_Gamble(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = """+1 Buy; Reveal the top card of your deck. If it's a Treasure
            or Action, you may play it. Otherwise, discard it."""
        self.name = "Gamble"
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        """Reveal the top card of your deck. If it's a Treasure
        or Action, you may play it. Otherwise, discard it."""
        nxt = player.next_card()
        player.output("Next card is {}".format(nxt.name))
        if nxt.isAction() or nxt.isTreasure():
            player.card_benefits(nxt)
        else:
            player.output("Card isn't a Treasure or Action - discarding")
        player.discard_card(nxt)


###############################################################################
class Test_Gamble(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Gamble"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Gamble"]

    def test_play_treasure(self):
        """Perform a Gamble with a treasure"""
        self.plr.add_coins(2)
        self.plr.deck.set("Gold")
        self.assertEqual(self.plr.get_buys(), 1)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.discardpile["Gold"])
        self.assertEqual(self.plr.get_coins(), 3)
        self.assertEqual(self.plr.get_buys(), 1)

    def test_play_action(self):
        """Perform a Gamble with an action"""
        self.plr.add_coins(2)
        self.plr.deck.set("Estate", "Estate", "Copper", "Moat")
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.discardpile["Moat"])
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertEqual(self.plr.hand.size(), 5 + 2)
        self.assertEqual(self.plr.get_buys(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
