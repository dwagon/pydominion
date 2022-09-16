#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Diplomat"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Diplomat(Card.Card):
    """Diplomat"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+2 Cards; If you have 5 or fewer cards in hand (after drawing), +2 Actions.
            When another player plays an Attack card, you may first reveal this from a hand of
            5 or more cards, to draw 2 cards then discard 3."""
        self.name = "Diplomat"
        self.cards = 2
        self.cost = 4

    def special(self, game, player):
        """If you have 5 or fewer cards in hand (after drawing), +2 Actions."""
        if player.hand.size() <= 5:
            player.add_actions(2)

    def hook_underAttack(self, game, player, attacker):
        """Reaction"""
        if player.hand.size() < 5:
            return
        react = player.plr_choose_options(
            "Reveal Diplomat to draw 2 cards then discard 3",
            ("Reveal Diplomat", True),
            ("Don't do anything", False),
        )
        if react:
            diplo = player.hand["Diplomat"]
            player.reveal_card(diplo)
            player.pickup_cards(2)
            player.plr_discard_cards(num=3)


###############################################################################
class Test_Diplomat(unittest.TestCase):
    """Test Diplomat"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Diplomat", "Militia"])
        self.g.start_game()
        self.plr, self.att = self.g.player_list()
        self.card = self.g["Diplomat"].remove()

    def test_play_small(self):
        """Play the Diplomat with a small hand"""
        self.plr.hand.set("Estate", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2 + 2)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_play_big(self):
        """Play the Diplomat with a big hand"""
        self.plr.hand.set("Estate", "Copper", "Duchy", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 4 + 2)
        self.assertEqual(self.plr.actions.get(), 0)

    def test_react(self):
        """React to an attack"""
        self.plr.hand.set("Gold", "Silver", "Province", "Duchy", "Copper")
        self.plr.add_card(self.card, "hand")
        militia = self.g["Militia"].remove()
        self.att.add_card(militia, "hand")
        self.plr.test_input = [
            "Reveal",
            "Discard Gold",  # Diplomat actions
            "Silver",
            "Province",
            "Finish",
            "Discard Duchy",  # Militia actions
            "Diplomat",
            "Finish",
        ]
        self.att.play_card(militia)
        self.assertEqual(self.plr.hand.size(), 3)
        self.assertEqual(self.plr.discardpile.size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
