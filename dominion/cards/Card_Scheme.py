#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Scheme(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = """+1 Card +1 Action; At the start of Clean-up this turn,
            you may choose an Action card you have in play. If you discard it from play
            this turn, put it on your deck."""
        self.name = "Scheme"
        self.cards = 1
        self.actions = 1
        self.cost = 3

    def hook_cleanup(self, game, player):
        actions = [c for c in player.played if c.isAction()]
        card = player.card_sel(
            cardsrc=actions, prompt="Select an action to put back on your deck"
        )
        if card:
            player.add_card(card[0], "topdeck")
            player.played.remove(card[0])


###############################################################################
class Test_Scheme(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Scheme", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Scheme"].remove()

    def test_play(self):
        """Play a scheme"""
        self.plr.add_card(self.card, "hand")
        self.plr.set_played("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 1)
        self.plr.test_input = ["moat"]
        self.plr.cleanup_phase()
        self.assertIn("Moat", self.plr.hand)
        self.assertIn("Scheme", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
