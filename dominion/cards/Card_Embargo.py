#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Embargo(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = """+2 Coin; Trash this. If you did, add an Embargo token
            to a Supply pile. (For the rest of the game, when a player buys a
            card from that pile, they gain a Curse.)"""
        self.name = "Embargo"
        self.required_cards = ["Curse"]
        self.coin = 2
        self.cost = 2

    def special(self, game, player):
        trash = player.plrChooseOptions(
            "Trash this card?",
            ("Keep this card", False),
            ("Trash this card to embargo", True),
        )
        if not trash:
            return
        player.trash_card(self)
        piles = list(game.cardpiles.values())
        piles.sort()
        card = player.cardSel(cardsrc=piles, prompt="Which stack to embargo")
        game[card[0].name].embargo()


###############################################################################
class Test_Embargo(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Embargo"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Embargo"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["trash", "Select Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.g["Silver"].embargo_level, 1)
        self.assertIsNotNone(self.g.in_trash("Embargo"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
