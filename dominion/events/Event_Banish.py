#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Banish """

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Banish(Event.Event):
    """Banish"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Exile any number of cards with the same name from your hand."
        self.name = "Banish"
        self.cost = 4

    def special(self, game, player):
        cardnames = {_.name for _ in player.hand}
        options = [("Exile nothing", None)]
        for cname in cardnames:
            options.append((f"Exile {cname} ({player.hand.count(cname)} in hand)", cname))
        card = player.plr_choose_options("Pick a card to exile", *options)
        if card is None:
            return
        if player.hand.count(card) == 1:
            for crd in player.hand:
                if crd.name == card:
                    player.exile_card(crd)
                    break
        else:
            options = []
            for i in range(player.hand.count(card) + 1):
                options.append((f"Exile {i} {card}", i))
            count = player.plr_choose_options("How many to exile", *options)
            for _ in range(count):
                for crd in player.hand:
                    if crd.name == card:
                        player.exile_card(crd)
                        break


###############################################################################
class Test_Banish(unittest.TestCase):
    """Test Banish"""

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
        self.plr.coins.add(4)
        self.plr.hand.set("Estate", "Estate", "Estate", "Duchy")
        self.plr.test_input = ["Estate", "2"]
        self.plr.perform_event(self.card)
        self.assertIn("Estate", self.plr.exilepile)
        self.assertIn("Estate", self.plr.hand)

    def test_Banish_single(self):
        """Use Banish"""
        self.plr.coins.add(4)
        self.plr.hand.set("Estate", "Estate", "Estate", "Duchy")
        self.plr.test_input = ["Duchy"]
        self.plr.perform_event(self.card)
        self.assertIn("Duchy", self.plr.exilepile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
