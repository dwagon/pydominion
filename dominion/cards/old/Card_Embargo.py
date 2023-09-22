#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Embargo"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Embargo(Card.Card):
    """Embargo"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+2 Coin; Trash this. If you did, add an Embargo token
            to a Supply pile. (For the rest of the game, when a player buys a
            card from that pile, they gain a Curse.)"""
        self.name = "Embargo"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 2

    def special(self, game, player):
        """Embargo Special"""
        trash = player.plr_choose_options(
            "Trash this card?",
            ("Keep this card", False),
            ("Trash this card to embargo", True),
        )
        if not trash:
            return
        player.trash_card(self)
        card_pile = player.card_pile_sel(prompt="Which stack to embargo")
        game.card_piles[card_pile[0]].embargo()


###############################################################################
class TestEmbargo(unittest.TestCase):
    """Test Embargo"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Embargo"], oldcards=True)
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Embargo")

    def test_play(self):
        """Test playing Embargo"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash", "Select Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.g.card_piles["Silver"].embargo_level, 1)
        self.assertIn("Embargo", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
