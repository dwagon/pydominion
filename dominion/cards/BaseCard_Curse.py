#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Curse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.DOMINION
        self.desc = "-1 VP"
        self.basecard = True
        self.playable = False
        self.purchasable = True
        self.name = "Curse"
        self.cost = 0
        self.victory = -1

    @classmethod
    def calc_numcards(cls, game):
        if game.numplayers == 1:
            return 10
        return 10 * (game.numplayers - 1)

    def special(self, game, player):
        if "Charlatan" in game.card_piles:
            player.coins.add(1)

    def setup(self, game):
        if "Charlatan" in game.card_piles:
            self.cardtype = [Card.CardType.VICTORY, Card.CardType.TREASURE]
            self.desc = "-1 VP; +$1"


###############################################################################
class Test_Curse(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Witch"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Curse")

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)

    def test_have(self):
        self.plr.add_card(self.card)
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Curse"], -1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
