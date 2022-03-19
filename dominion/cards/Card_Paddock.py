#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Paddock """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Paddock(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = """+2 Coin; Gain 2 Horses. +1 Action per empty Supply pile."""
        self.name = "Paddock"
        self.coin = 2
        self.cost = 5
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        player.gain_card("Horse")
        player.gain_card("Horse")
        empties = sum([1 for st in game.cardpiles if game[st].is_empty()])
        player.add_actions(empties)


###############################################################################
class Test_Paddock(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Paddock", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Paddock"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard_one_stack(self):
        while True:
            c = self.g["Moat"].remove()
            if not c:
                break
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_discard("Horse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
