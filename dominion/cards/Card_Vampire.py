#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Vampire(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT, Card.TYPE_ATTACK, Card.TYPE_DOOM]
        self.base = Game.NOCTURNE
        self.desc = "Each other player receives the next Hex.  Gain a card costing up to 5 other than a Vampire.  Exchange this for a Bat."
        self.name = "Vampire"
        self.cost = 5
        self.required_cards = [("Card", "Bat")]

    def night(self, game, player):
        for pl in player.attack_victims():
            pl.output(f"{player.name}'s Vampire hexed you")
            pl.receive_hex()
        player.plr_gain_card(5, exclude=["Vampire"])
        player.replace_card(self, "Bat")


###############################################################################
class Test_Vampire(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2, initcards=["Vampire"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Vampire"].remove()
        self.plr.add_card(self.card, "hand")
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play(self):
        self.plr.test_input = ["Get Duchy"]
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.play_card(self.card)
        self.assertTrue(self.vic.has_state("Deluded"))
        self.assertIsNotNone(self.plr.in_discard("Duchy"))
        self.assertIsNone(self.plr.in_discard("Vampire"))
        self.assertIsNotNone(self.plr.in_discard("Bat"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
