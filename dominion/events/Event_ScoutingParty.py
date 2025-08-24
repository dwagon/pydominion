#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event


###############################################################################
class Event_ScoutingParty(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Buy, Look at the top 5 cards of your deck. Discard 3 of them and put the rest back in any order"
        self.name = "Scouting Party"
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        cards = []
        for _ in range(5):
            cards.append(player.next_card())
        discards = player.card_sel(num=3, cardsrc=cards, force=True, prompt="Select cards to discard")
        # TODO - Put cards back in specific order
        for card in cards:
            if card not in discards:
                player.add_card(card, Piles.TOPDECK)
            else:
                player.add_card(card, Piles.DISCARD)


###############################################################################
class Test_ScoutingParty(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Scouting Party"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Scouting Party"]

    def test_play(self):
        """Perform a Scouting Party"""
        self.plr.coins.add(2)
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.test_input = ["estate", "duchy", "province", "finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DECK][0].name, "Gold")
        self.assertEqual(self.plr.piles[Piles.DECK][1].name, "Silver")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
