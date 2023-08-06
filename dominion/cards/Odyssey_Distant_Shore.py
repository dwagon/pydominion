#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Distant_Shore"""

import unittest
from dominion import Game, Card


###############################################################################
class Card_Distant_Shore(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.VICTORY,
            Card.CardType.ODYSSEY,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 6
        self.name = "Distant Shore"
        self.cards = 2
        self.actions = 1
        self.victory = 2
        self.desc = """ +2 Cards; +1 Action; Gain an Estate. 2VP"""

    def special(self, game, player):
        player.gain_card("Estate")


###############################################################################
class Test_Distant_Shore(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g["Odysseys"].remove()
            if card.name == "Distant Shore":
                break
        self.card = card

    def test_play(self):
        """Play the card"""
        hndsz = self.plr.hand.size()
        actions = self.plr.actions.get()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), hndsz + 2)
        self.assertEqual(self.plr.actions.get(), actions)
        self.assertIn("Estate", self.plr.discardpile)
        self.assertEqual(self.plr.get_score_details()["Distant Shore"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
