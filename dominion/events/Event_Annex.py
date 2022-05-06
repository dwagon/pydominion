#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Annex(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Look through your discard pile. Shuffle all but up to 5 cards from it into your deck. Gain a Duchy."
        self.name = "Annex"
        self.debtcost = 8

    def special(self, game, player):
        if player.discardpile.size() <= 5:
            player.output("Not enough cards to choose")
            return
        cards = player.card_sel(
            num=5, cardsrc="discard", prompt="Select 5 cards to leave in discard pile"
        )
        keep = []
        for card in player.discardpile:
            if card in cards:
                keep.append(card)
            else:
                player.add_card(card, "deck")
        player.deck.shuffle()
        player.discardpile.set()
        for card in keep:
            player.add_card(card, "discard")
        if player.gain_card("Duchy"):
            player.output("Gained a Duchy")


###############################################################################
class Test_Annex(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            eventcards=["Annex"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Annex"]

    def test_play(self):
        """Perform Annex"""
        self.plr.discardpile.set("Gold", "Silver", "Copper", "Province", "Moat", "Estate")
        self.plr.test_input = [
            "Silver",
            "Copper",
            "Province",
            "Moat",
            "Estate",
            "Finish",
        ]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.debt, 8)
        self.assertIsNotNone(self.plr.discardpile["Duchy"])
        self.assertNotIn("Gold", self.plr.discardpile)
        self.assertIn("Gold", self.plr.deck)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
