#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Carpenter """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Carpenter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALLIES
        self.name = "Carpenter"
        self.cost = 4

    @classmethod
    def desc(cls, player):
        if player.phase == "buy":
            return """If no Supply piles are empty, +1 Action and gain a card
                costing up to $4.  Otherwise, trash a card from your hand and
                gain a card costing up to $2 more than it."""
        empties = sum([1 for st in player.game.cardpiles if player.game[st].is_empty()])
        if empties:
            return """Trash a card from your hand and gain
                a card costing up to $2 more than it."""
        return """+1 Action and gain a card costing up to $4."""

    def special(self, game, player):
        empties = sum([1 for st in game.cardpiles if game[st].is_empty()])
        if not empties:
            player.add_actions(1)
            player.plr_gain_card(4)
        else:
            tr = player.plr_trash_card()
            player.plr_gain_card(tr[0].cost+2)


###############################################################################
class Test_Carpenter(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Carpenter", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Carpenter"].remove()

    def test_play_full(self):
        """Play the card with no empties"""
        self.plr.add_card(self.card, "hand")
        acts = self.plr.get_actions()
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), acts)
        self.assertIn("Silver", self.plr.discardpile)

    def test_play_empty(self):
        """Play the card with an empty"""
        self.plr.hand.set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        while True:
            c = self.g["Moat"].remove()
            if not c:
                break
        self.plr.test_input = ["Trash Copper", "Get Estate"]
        self.plr.play_card(self.card)
        self.assertIn("Estate", self.plr.discardpile)
        self.assertIn("Copper", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
