#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Idol(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_ATTACK, Card.TYPE_FATE]
        self.base = Game.NOCTURNE
        self.desc = """2 Coin; When you play this, if you then have an odd number
            of Idols in play, receive a Boon; if an even number, each other player
            gains a Curse."""
        self.name = "Idol"
        self.coin = 2
        self.cost = 5
        self.required_cards = ["Curse"]

    def special(self, game, player):
        idols = player.played.count("Idol") + player.hand.count("Idol")
        if idols % 2 == 1:  # Odd
            player.receive_boon()
        else:  # Even
            for pl in player.attack_victims():
                pl.output(f"{player.name}'s Idol cursed you")
                pl.gain_card("Curse")


###############################################################################
class Test_Idol(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Idol"], badcards=["Druid"])
        self.g.start_game()
        for b in self.g.boons:
            if b.name == "The Mountain's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Idol"].remove()

    def test_play_even(self):
        """Play an even number of Idol"""
        self.plr.played.set("Idol", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIn("Curse", self.vic.discardpile)
        self.assertNotIn("Silver", self.plr.discardpile)

    def test_play_odd(self):
        """Play an odd number of Idol"""
        self.plr.played.set("Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertNotIn("Curse", self.vic.discardpile)
        self.assertIn("Silver", self.plr.discardpile)  # From Mountain boon


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
