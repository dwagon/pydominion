#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Library(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = """Draw until you have 7 cards in hand. You may set aside
            any Action cards drawn this way, as you draw them; discard the set
            aside cards after you finish drawing"""
        self.name = "Library"
        self.cost = 5

    def special(self, game, player):
        """Draw until you have 7 cards in your hand. You may set
        aside action cards drawn this way, as you draw them; discard
        the set aside cards after you finish drawing"""
        while player.hand.size() < 7:
            c = player.next_card()
            if c.isAction():
                if self.discardChoice(player, c):
                    player.add_card(c, "discard")
                    continue
            player.pickup_card(c)

    def discardChoice(self, plr, card):
        ans = plr.plr_choose_options(
            "Picked up %s. Discard from library?" % card.name,
            ("Discard %s" % card.name, True),
            ("Keep %s" % card.name, False),
        )
        return ans


###############################################################################
class Test_Library(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Library", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Library"].remove()
        self.plr.add_card(self.card, "hand")

    def test_noactions(self):
        """Play a library where no actions are drawn"""
        self.plr.set_deck("Duchy", "Copper", "Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 7)

    def test_actions_discard(self):
        """Play a library where actions are drawn and discarded"""
        self.plr.set_deck("Duchy", "Moat", "Gold")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, "Moat")
        self.assertEqual(self.plr.hand.size(), 7)

    def test_actions_keep(self):
        """Play a library where actions are drawn and kept"""
        self.plr.set_deck("Duchy", "Moat", "Gold")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.deck[-1].name, "Duchy")
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertTrue(self.plr.in_hand("Moat"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
