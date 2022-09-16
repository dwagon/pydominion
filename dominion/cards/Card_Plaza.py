#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Plaza(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = (
            "+1 Card, +2 Actions. You may discard a Treasure card. If you do, take a Coffer."
        )
        self.name = "Plaza"
        self.actions = 2
        self.cards = 1
        self.cost = 4

    def special(self, game, player):
        treasures = [c for c in player.hand if c.isTreasure()]
        if treasures:
            disc = player.plr_discard_cards(
                num=1, cardsrc=treasures, prompt="Discard a treasure to gain a Coffer"
            )
            if disc:
                player.coffers.add(1)


###############################################################################
class Test_Plaza(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Plaza", "Pooka"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Plaza"].remove()

    def test_play(self):
        """Play a plaza"""
        try:
            self.plr.coffers.set(0)
            self.plr.hand.set("Gold")
            self.plr.test_input = ["discard gold"]
            self.plr.add_card(self.card, "hand")
            self.plr.play_card(self.card)
            self.assertEqual(self.plr.coffers.get(), 1)
            self.assertEqual(self.plr.actions.get(), 2)
            self.assertEqual(self.plr.hand.size(), 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
