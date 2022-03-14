#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea
from dominion import Game


###############################################################################
class Card_Necromancer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION]
        self.base = Game.NOCTURNE
        self.desc = "Play a non-Duration Action card from the trash, leaving it there."
        self.name = "Necromancer"
        self.cost = 4
        self.required_cards = [
            ("Card", "Zombie Apprentice"),
            ("Card", "Zombie Mason"),
            ("Card", "Zombie Spy"),
        ]

    def special(self, game, player):
        act = [
            _
            for _ in game.trashpile
            if _.isAction() and not _.isDuration() and _ not in game._necromancer
        ]
        card = player.card_sel(cardsrc=act, prompt="Select Action card from Trash")
        game._necromancer.add(card[0])
        player.play_card(card[0], discard=False, costAction=False)

    def setup(self, game):
        game._necromancer = PlayArea.PlayArea()

    def hook_cleanup(self, game, player):
        print("end")
        game._necromancer = PlayArea.PlayArea()


###############################################################################
class Test_Necromancer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Necromancer", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Necromancer"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Necromancer"""
        self.plr.set_deck("Gold", "Silver")
        self.plr.test_input = ["Zombie Spy", "Keep"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_hand("Silver"))  # From Zombie Spy


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
