#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Overgrown_Estate """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Overgrown_Estate(Card.Card):
    """ Overgrown Estate """
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_VICTORY, Card.TYPE_SHELTER]
        self.base = Game.DARKAGES
        self.desc = "0VP; When you trash this, +1 Card."
        self.name = "Overgrown Estate"
        self.cost = 1
        self.victory = 0
        self.purchasable = False

    def hook_trashThisCard(self, game, player):
        player.pickup_card()


###############################################################################
class Test_Overgrown_Estate(unittest.TestCase):
    """ Test Overgrown Estate """
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Shelters"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """ Test Play """
        self.plr.deck.set("Province")
        self.plr.hand.set("Overgrown Estate")
        card = self.plr.hand["Overgrown Estate"]
        self.plr.trash_card(card)
        self.assertIn("Province", self.plr.hand)
        self.assertIn("Overgrown Estate", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
