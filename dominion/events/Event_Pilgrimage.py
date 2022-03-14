#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Pilgrimage(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.EMPIRES
        self.desc = """Once per turn: Turn your Journey token over; then if it's face up,
        choose up to 3 differently named cards you have in play and gain a copy of each."""
        self.name = "Pilgrimage"
        self.cost = 4

    def special(self, game, player):
        if not player.do_once("Pilgrimage"):
            player.output("Already performed a Pilgrimage this turn")
            return
        if not player.flip_journey_token():
            player.output("Flipped Journey token to face down")
            return
        cardnames = {c.name for c in player.played if c.purchasable}
        selected = []
        while True:
            options = [{"selector": "0", "print": "Finish", "opt": None}]
            index = 1
            for cn in cardnames:
                options.append({"selector": "%d" % index, "print": cn, "opt": cn})
                index += 1
            choice = player.userInput(options, "Select a card to gain - up to 3!")
            if choice["opt"]:
                selected.append(choice["opt"])
                cardnames.remove(choice["opt"])
            else:
                break
            if len(selected) == 3:
                break
        for card in selected:
            player.gain_card(card)
            player.output("Gained a %s" % card)


###############################################################################
class Test_Pilgrimage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, eventcards=["Pilgrimage"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events["Pilgrimage"]

    def test_play(self):
        """Perform a Pilgrimage"""
        self.plr.set_played("Moat", "Silver", "Gold", "Copper", "Duchy")
        self.plr.test_input = ["moat", "silver", "finish"]
        self.plr.journey_token = False
        self.plr.add_coins(4)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.in_discard("Moat"))
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertTrue(self.plr.journey_token)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
