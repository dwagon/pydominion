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
        nxt = player.nextCard()
        player.output("Next card is {}".format(nxt.name))
        if nxt.isAction() or nxt.isTreasure():
            player.card_benefits(nxt)
        else:
            player.output("Card isn't a Treasure or Action - discarding")
        player.discardCard(nxt)


###############################################################################
class Test_Gamble(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, eventcards=["Gamble"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Gamble"]

    def test_play_treasure(self):
        """Perform a Gamble with a treasure"""
        self.plr.addCoin(2)
        self.plr.setDeck("Gold")
        self.assertEqual(self.plr.get_buys(), 1)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Gold"))
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertEqual(self.plr.get_buys(), 1)

    def test_play_action(self):
        """Perform a Gamble with an action"""
        self.plr.addCoin(2)
        self.plr.setDeck("Estate", "Estate", "Copper", "Moat")
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Moat"))
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.hand.size(), 5 + 2)
        self.assertEqual(self.plr.get_buys(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
