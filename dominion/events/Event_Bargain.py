#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Bargain"""

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Bargain(Event.Event):
    """Bargain"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Gain a non-Victory card costing up to $5. Each other player gains a Horse."
        self.name = "Bargain"
        self.cost = 4
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        player.plr_gain_card(
            5,
            types={
                Card.CardType.ACTION: True,
                Card.CardType.TREASURE: True,
                Card.CardType.NIGHT: True,
            },
        )
        for plr in game.player_list():
            if plr != player:
                plr.output(f"Gained a horse from {player.name}'s Bargain")
                plr.gain_card("Horse")


###############################################################################
class Test_Bargain(unittest.TestCase):
    """Test Bargain"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, eventcards=["Bargain"], initcards=["Moat"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.events["Bargain"]

    def test_use(self):
        """Use Bargain"""
        self.plr.coins.set(4)
        self.plr.test_input = ["Moat"]
        self.plr.perform_event(self.card)
        self.g.print_state()
        self.assertIn("Horse", self.oth.discardpile)
        self.assertIn("Moat", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
