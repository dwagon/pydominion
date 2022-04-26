#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sorceress"""


import unittest
from dominion import Game, Card


###############################################################################
class Card_Sorceress(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_AUGUR,  # pylint: disable=no-member
        ]
        self.base = Game.ALLIES
        self.cost = 5
        self.actions = 1
        self.name = "Sorceress"
        self.desc = """+1 Action; Name a card. Reveal the top card of your deck
            and put it into your hand. If it's the named card, each other player
            gains a Curse."""

    def special(self, game, player):
        pass


###############################################################################
class Test_Sorceress(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Augurs"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g["Augurs"].remove()
            if card.name == "Sorceress":
                break
        self.card = card

    def test_play(self):
        """Play a lich"""
        hndsz = self.plr.hand.size()
        self.plr.add_card(self.card, "hand")
        self.plr.set_discard("Estate", "Duchy", "Province", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.hand.size(), hndsz + 6)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_trash(self):
        """Trash the lich"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Silver"]
        self.g.set_trash("Silver")
        self.plr.trash_card(self.card)
        self.g.print_state()
        self.assertIsNone(self.g.in_trash("Sorceress"))
        self.assertIsNone(self.g.in_trash("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Sorceress"))
        self.assertIsNotNone(self.plr.in_discard("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
