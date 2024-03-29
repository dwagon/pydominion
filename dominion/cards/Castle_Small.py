#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_SmallCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.VICTORY,
            Card.CardType.CASTLE,
        ]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 5
        self.desc = (
            "Trash this or a Castle from your hand. If you do, gain a Castle. 2VP"
        )
        self.coin = 1
        self.name = "Small Castle"
        self.victory = 2
        self.pile = "Castles"

    def special(self, game, player):
        cards = [c for c in player.piles[Piles.HAND] if c.isCastle()] + [self]
        tr = player.plr_trash_card(
            prompt="Trash a Castle to gain another Castle", cardsrc=cards
        )
        if tr:
            newcast = player.gain_card("Castles")
            player.output("Gained %s" % newcast.name)


###############################################################################
class Test_SmallCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g.get_card_from_pile("Castles")
            if self.card.name == "Small Castle":
                break

    def test_play(self):
        """Play a castle - trash nothing"""
        self.plr.test_input = ["Finish"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Small Castle"], 2)

    def test_trash(self):
        """Play a castle - trash self"""
        self.plr.test_input = ["small"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
