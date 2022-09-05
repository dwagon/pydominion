#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Cardinal """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Cardinal(Card.Card):
    """Cardinal"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.MENAGERIE
        self.desc = """Each other player reveals the top 2 cards of their deck,
            Exiles one costing from 3 to 6, and discards the rest."""
        self.name = "Cardinal"
        self.cost = 4

    def special(self, game, player):
        for plr in player.attack_victims():
            exilecount = 0
            for _ in range(2):
                crd = plr.pickup_card()
                plr.reveal_card(crd)
                if 3 <= crd.cost <= 6 and not exilecount:
                    plr.exile_card(crd)
                    plr.output(f"{player.name}'s Cardinal exiled your {crd.name}")
                    exilecount += 1
                else:
                    plr.output(f"{player.name}'s Cardinal discarded your {crd.name}")
                    plr.discard_card(crd)


###############################################################################
class Test_Cardinal(unittest.TestCase):
    """Test Cardinal"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Cardinal", "Village"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g["Cardinal"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """ Test play """
        self.oth.deck.set("Silver", "Village")
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.oth.discardpile)
        self.assertIn("Village", self.oth.exilepile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
