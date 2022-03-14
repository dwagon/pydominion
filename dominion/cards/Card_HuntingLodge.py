#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Hunting_Lodge """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Hunting_Lodge(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = "+1 Card; +2 Actions; You may discard your hand for +5 Cards."
        self.name = "Hunting Lodge"
        self.cards = 1
        self.actions = 2
        self.cost = 5

    def special(self, game, player):
        disc = player.plrChooseOptions(
            "Discard hand?", ("Nope", False), ("Discard hand and draw 5 cards", True)
        )
        if disc:
            player.discard_hand()
            player.pickup_cards(5)


###############################################################################
class Test_Hunting_Lodge(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Hunting Lodge"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hunting Lodge"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a card and discard hand"""
        self.plr.test_input = ["Discard"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_playcard_keep(self):
        """Play a card and keep hand"""
        self.plr.test_input = ["Nope"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
