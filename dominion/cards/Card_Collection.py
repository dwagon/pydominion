#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Collection"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Collection(Card.Card):
    """Collection"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "$2; +1 Buy; This turn, when you gain an Action card, +1 VP."
        self.name = "Collection"
        self.buys = 1
        self.coin = 2
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        if card.isAction():
            player.add_score("Collection", 1)


###############################################################################
class Test_Collection(unittest.TestCase):
    """Test Collection"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Collection", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Collection")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        """Play Collection"""
        score = self.plr.get_score()
        self.plr.play_card(self.card)
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.get_score(), score + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
