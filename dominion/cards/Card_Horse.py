#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Horse """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Horse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards; +1 Action; Return this to its pile."
        self.name = "Horse"
        self.purchasable = False
        self.insupply = False
        self.actions = 1
        self.cards = 2
        self.cost = 0
        self.numcards = 30

    def special(self, game, player):
        player.discard_card(self)
        try:  # If Horse is played multiple times e.g. Kings Court
            player.played.remove(self)
            card = player.discardpile.remove(self)
            game["Horse"].add(card)
        except ValueError:
            pass


###############################################################################
class Test_Horse(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Horse"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Horse"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertNotIn("Horse", self.plr.played)
        self.assertEqual(self.plr.hand.size(), 5 + 2)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
