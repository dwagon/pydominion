#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sheepdog """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Sheepdog(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards; When you gain a card, you may play this from your hand."
        self.name = "Sheepdog"
        self.cards = 2
        self.cost = 3

    def hook_gain_card(self, game, player, card):
        player.play_card(self, costAction=False)


###############################################################################
class Test_Sheepdog(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sheepdog"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sheepdog"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2)

    def test_gain(self):
        """Gain a card"""
        self.plr.gain_card("Estate")
        self.g.print_state()
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
