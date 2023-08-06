#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sea_Witch"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_SeaWitch(Card.Card):
    """Sea Witch"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+2 Cards; Each other player gains a Curse.
            At the start of your next turn, +2 Cards, then discard 2 cards."""
        self.name = "Sea Witch"
        self.required_cards = ["Curse"]
        self.cards = 2
        self.cost = 5

    def special(self, game, player):
        for plr in player.attack_victims():
            player.output(f"{player.name}'s Sea Witch cursed you")
            player.output(f"{plr.name} got cursed")
            plr.gain_card("Curse")

    def duration(self, game, player):
        """+2 card, discard 2"""
        player.pickup_cards(2)
        player.plr_discard_cards(num=2, force=True)


###############################################################################
class Test_SeaWitch(unittest.TestCase):
    """Test Sea Witch"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Sea Witch"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Sea Witch"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a sea witch"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2)
        self.assertIn("Curse", self.vic.discardpile)
        self.plr.end_turn()
        self.plr.deck.set("Copper", "Silver", "Gold")
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Discard Estate", "Discard Duchy", "Finish"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 2 - 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
