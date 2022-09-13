#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Poacher """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Poacher(Card.Card):
    """Poacher"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+1 Card, +1 Action, +1 Coin. Discard a card per empty supply pile."
        self.name = "Poacher"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 4

    def special(self, game, player):
        empties = sum(1 for st in game.cardpiles if game[st].is_empty())
        if empties:
            player.plr_discard_cards(num=empties, force=True)


###############################################################################
class Test_Poacher(unittest.TestCase):
    """Test Poacher"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Poacher", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Poacher"].remove()

    def test_play(self):
        """Play card"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_empty(self):
        """Play card with an empty pile"""
        self.plr.hand.set("Gold", "Province")
        self.plr.add_card(self.card, "hand")
        while True:
            c = self.g["Moat"].remove()
            if not c:
                break
        self.plr.test_input = ["Discard Gold"]
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
