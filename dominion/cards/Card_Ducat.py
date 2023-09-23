#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Ducat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.RENAISSANCE
        self.buys = 1
        self.name = "Ducat"
        self.cost = 2

    ###########################################################################
    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return "+1 Coffers; +1 Buy; When you gain this, you may trash a Copper from your hand."
        return "+1 Coffers; +1 Buy"

    ###########################################################################
    def special(self, game, player):
        player.coffers.add(1)

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        cu = player.piles[Piles.HAND]["Copper"]
        if cu:
            player.plr_trash_card(cardsrc=[cu], num=1)
        else:
            player.output("No Coppers")


###############################################################################
class Test_Ducat(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Ducat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        card = self.g.get_card_from_pile("Ducat")
        self.plr.coffers.set(0)
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.assertEqual(self.plr.coffers.get(), 1)
        self.assertEqual(self.plr.buys.get(), 1 + 1)

    def test_gain_trash(self):
        self.plr.test_input = ["Copper"]
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.gain_card("Ducat")

    def test_gain_nothing(self):
        self.plr.piles[Piles.HAND].set("Silver")
        self.plr.gain_card("Ducat")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
