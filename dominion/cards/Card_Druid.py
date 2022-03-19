#!/usr/bin/env python

import unittest
import random
from dominion import Card
from dominion import PlayArea
from dominion import Game


###############################################################################
class Card_Druid(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_FATE]
        self.base = Game.NOCTURNE
        self.desc = "+1 Buy; Receive one of the set-aside Boons"
        self.name = "Druid"
        self.buys = 1
        self.cost = 2

    def setup(self, game):
        game._druid_area = PlayArea.PlayArea([])
        random.shuffle(game.boons)
        for _ in range(3):
            game._druid_area.add(game.boons.pop())

    def special(self, game, player):
        options = []
        for i in range(3):
            sel = "%d" % i
            bn = list(game._druid_area)[i]
            toprint = "Receive {}: {}".format(bn.name, bn.description(player))
            options.append({"selector": sel, "print": toprint, Card.TYPE_BOON: bn})
        b = player.user_input(options, "Which boon? ")
        player.receive_boon(boon=b[Card.TYPE_BOON], discard=False)


###############################################################################
class Test_Druid(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Druid", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Druid"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Druid"""
        self.plr.test_input = ["0", "0"]
        self.plr.play_card(self.card)
        self.assertGreaterEqual(self.plr.get_buys(), 2)

    def test_setaside(self):
        """Test that we don't get a set aside boon"""
        setaside = {_.name for _ in self.g._druid_area}  # pylint: disable=no-member
        left = {_.name for _ in self.g.boons}
        if setaside.intersection(left):
            self.fail("Set aside boons not set aside")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
