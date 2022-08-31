#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Pirate """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Pirate(Card.Card):
    """Pirate"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION, Card.TYPE_REACTION]
        self.base = Game.SEASIDE
        self.desc = """At the start of your next turn, gain a Treasure costing up
            to $6 to your hand.
            When any player gains a Treasure, you may play this from your hand."""
        self.name = "Pirate"
        self.cost = 5

    def duration(self, game, player):
        """gain a Treasure costing up to $6 to your hand"""
        # Discard first to avoid the gained card triggering the pirate again
        player.move_card(self, "played")
        player.plr_gain_card(cost=6, types={Card.TYPE_TREASURE: True}, destination="hand")

    def hook_allplayers_gain_card(self, game, player, owner, card):
        """When any player gains a Treasure, you may play this from your hand"""
        if not card.isTreasure():
            return
        if self.location != "hand":
            return
        owner.output(f"Player {player.name} gained a treasure ({card.name})")
        gain = owner.plr_choose_options(
            "Do you wish to play your Pirate?",
            ("Do Nothing", False),
            ("Gain a treasure costing up to $6 to your hand", True),
        )
        if not gain:
            return
        owner.move_card(self, "played")
        owner.plr_gain_card(cost=6, types={Card.TYPE_TREASURE: True}, destination="hand")


###############################################################################
class Test_Pirate(unittest.TestCase):
    """Test Pirate"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Pirate"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g["Pirate"].remove()

    def test_playcard(self):
        """Play a pirate"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.test_input = ["Get Gold"]
        self.plr.start_turn()
        self.assertEqual(self.plr.durationpile.size(), 0)
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Pirate", self.plr.played)

    def test_react_treasure(self):
        """Play a pirate through a reaction"""
        self.plr.hand.set("Pirate")
        self.plr.test_input = ["Gain a treasure", "Get Gold"]
        self.oth.gain_card("Silver")
        self.assertIn("Gold", self.plr.hand)
        self.assertIn("Pirate", self.plr.played)

    def test_react_not_treasure(self):
        """Play a pirate through a reaction, but not a treasure"""
        self.plr.hand.set("Pirate")
        self.plr.test_input = ["Gain a treasure", "Get Gold"]
        self.oth.gain_card("Estate")
        self.assertNotIn("Gold", self.plr.hand)
        self.assertNotIn("Pirate", self.plr.played)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
