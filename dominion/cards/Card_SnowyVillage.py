#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Snowy_Village """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_SnowyVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Card; +4 Actions; +1 Buy; Ignore any further +Actions you get this turn."
        self.name = "Snowy Village"
        self.cost = 3
        self.cards = 1
        self.actions = 4
        self.buys = 1

    def special(self, game, player):
        player.misc["no_actions"] = True


###############################################################################
class Test_SnowyVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Snowy Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Snowy Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 4)
        self.assertEqual(self.plr.buys.get(), 1 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 4 - 1)  # -1 for playing card
        self.assertEqual(self.plr.buys.get(), 1 + 1 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
