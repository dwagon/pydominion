#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Banish """

import unittest
from dominion import Game, Event


###############################################################################
class Event_Banish(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Exile any number of cards with the same name from your hand."
        self.name = "Banish"
        self.cost = 4

    def special(self, game, player):
        cardnames = {_.name for _ in player.hand}
        options = [("Exile nothing", None)]
        for cname in cardnames:
            options.append(
                ("Exile {} ({} in hand)".format(cname, player.hand.count(cname)), cname)
            )
        card = player.plr_choose_options("Pick a card to exile", *options)
        if card is None:
            return
        if player.hand.count(card) == 1:
            for crd in player.hand:
                if crd.name == card:
                    player.exile_card(crd)
                    player.hand.remove(crd)
                    break
        else:
            options = []
            for i in range(player.hand.count(card) + 1):
                options.append(("Exile {} {}".format(i, card), i))
            count = player.plr_choose_options("How many to exile", *options)
            for _ in range(count):
                for crd in player.hand:
                    if crd.name == card:
                        player.exile_card(crd)
                        player.hand.remove(crd)
                        break


###############################################################################
class Test_Banish(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            eventcards=["Banish"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Banish"]

    def test_Banish_multi(self):
        """Use Banish"""
        self.plr.add_coins(4)
        self.plr.set_hand("Estate", "Estate", "Estate", "Duchy")
        self.plr.test_input = ["Estate", "2"]
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.in_exile("Estate"))
        self.assertIn("Estate", self.plr.hand)

    def test_Banish_single(self):
        """Use Banish"""
        self.plr.add_coins(4)
        self.plr.set_hand("Estate", "Estate", "Estate", "Duchy")
        self.plr.test_input = ["Duchy"]
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.in_exile("Duchy"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
