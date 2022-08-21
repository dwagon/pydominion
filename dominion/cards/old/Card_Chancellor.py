#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Chancellor """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Chancellor(Card.Card):
    """Chancellor"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+2 Coin; You may immediately put your deck into your discard pile."
        self.name = "Chancellor"
        self.coin = 2
        self.cost = 3

    def special(self, game, player):  # pylint: disable=unused-argument
        """Chancellor Special"""
        disc = player.plr_choose_options(
            "Discard deck?", ("Don't Discard", False), ("Discard Deck", True)
        )
        if disc:
            for crd in player.deck:
                player.add_card(crd, "discard")
                player.deck.remove(crd)


###############################################################################
class Test_Chancellor(unittest.TestCase):
    """Test Chancellor"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Chancellor"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g["Chancellor"].remove()
        self.plr.hand.set("Estate")
        self.plr.add_card(self.ccard, "hand")

    def test_nodiscard(self):
        """Play Chancellor and choose not to discard"""
        self.plr.deck.set("Copper", "Silver", "Gold")
        self.plr.discardpile.set("Estate", "Duchy", "Province")
        self.plr.test_input = ["Don't discard"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.deck.size(), 3)
        self.assertEqual(self.plr.discardpile.size(), 3)

    def test_discard(self):
        """Play Chancellor and choose to discard deck"""
        self.plr.deck.set("Copper", "Silver", "Gold")
        self.plr.discardpile.set("Estate", "Duchy", "Province")
        self.plr.test_input = ["discard deck"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.deck.size(), 0)
        self.assertEqual(self.plr.discardpile.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
