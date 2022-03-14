#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Royalseal(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.PROSPERITY
        self.desc = "+2 Coin. While this is in play, when you gain a card, you may put that card on top of your deck."
        self.playable = False
        self.name = "Royal Seal"
        self.cost = 5
        self.coin = 2

    def hook_gain_card(self, game, player, card):
        """While this is in play, when you gain a card, you may
        put that card on top of your deck"""
        mod = {}
        deck = player.plrChooseOptions(
            "Where to put %s?" % card.name,
            ("Put %s on discard" % card.name, False),
            ("Put %s on top of deck" % card.name, True),
        )
        if deck:
            player.output("Putting %s on deck due to Royal Seal" % card.name)
            mod["destination"] = "topdeck"
        return mod


###############################################################################
class Test_Royalseal(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Royal Seal"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Royal Seal"].remove()

    def test_play(self):
        """Play a Royal Seal"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_discard(self):
        """Have a Royal Seal  - discard the gained card"""
        self.plr.set_played("Royal Seal")
        self.plr.test_input = ["discard"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertEqual(self.plr.discardpile[0].name, "Gold")
        self.assertFalse(self.plr.in_hand("Gold"))

    def test_deck(self):
        """Have a Royal Seal  - the gained card on the deck"""
        self.plr.set_played("Royal Seal")
        self.plr.test_input = ["deck"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.deck[-1].name, "Gold")
        self.assertIsNone(self.plr.in_hand("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
