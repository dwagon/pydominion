#!/usr/bin/env python
# pylint: disable=protected-access

import unittest
import random
from dominion import Card
from dominion import PlayArea
from dominion import Game, Piles


###############################################################################
class Card_Druid(Card.Card):
    """Druid"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
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
            sel = f"{i}"
            bn = list(game._druid_area)[i]
            toprint = f"Receive {bn.name}: {bn.description(player)}"
            options.append({"selector": sel, "print": toprint, "boon": bn})
        b = player.user_input(options, "Which boon? ")
        player.receive_boon(boon=b["boon"], discard=False)


###############################################################################
class Test_Druid(unittest.TestCase):
    """Test Druid"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Druid", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Druid"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a Druid"""
        self.plr.test_input = ["0", "0"]
        self.plr.play_card(self.card)
        self.assertGreaterEqual(self.plr.buys.get(), 2)

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
