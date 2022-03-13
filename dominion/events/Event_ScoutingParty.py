#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_ScoutingParty(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "+1 Buy, Look at the top 5 cards of your deck. Discard 3 of them and put the rest back in any order"
        self.name = "Scouting Party"
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        cards = []
        for _ in range(5):
            cards.append(player.nextCard())
        discards = player.cardSel(
            num=3, cardsrc=cards, force=True, prompt="Select cards to discard"
        )
        # TODO - Put cards back in specific order
        for card in cards:
            if card not in discards:
                player.addCard(card, "topdeck")
            else:
                player.addCard(card, "discard")


###############################################################################
class Test_ScoutingParty(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=["Scouting Party"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Scouting Party"]

    def test_play(self):
        """Perform a Scouting Party"""
        self.plr.addCoin(2)
        self.plr.set_deck("Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.test_input = ["estate", "duchy", "province", "finish"]
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.deck[0].name, "Gold")
        self.assertEqual(self.plr.deck[1].name, "Silver")
        self.assertEqual(self.plr.discardpile.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
