#!/usr/bin/env python

import unittest
import Game
import Card
from PlayArea import PlayArea


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
        card = player.cardSel(cardsrc=act, prompt="Select Action card from Trash")
        game._necromancer.add(card[0])
        player.playCard(card[0], discard=False, costAction=False)

    def setup(self, game):
        game._necromancer = PlayArea()

    def hook_cleanup(self, game, player):
        print("end")
        game._necromancer = PlayArea()


###############################################################################
class Test_Necromancer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Necromancer", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Necromancer"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play a Necromancer"""
        self.plr.setDeck("Gold", "Silver")
        self.plr.test_input = ["Zombie Spy", "Keep"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_hand("Silver"))  # From Zombie Spy


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
