#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Cultist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_LOOTER]
        self.base = Game.DARKAGES
        self.desc = """+2 Cards; Each other player gains a Ruins. You may play
            a Cultist from your hand.  When you trash this, +3 Cards."""
        self.name = "Cultist"
        self.cost = 5
        self.cards = 2

    def special(self, game, player):
        """Each other play gains a Ruins. You may play a Cultist
        from your hand."""
        for plr in player.attack_victims():
            plr.output("Gained a ruin from %s's Cultist" % player.name)
            plr.gain_card("Ruins")
        cultist = player.hand["Cultist"]
        if cultist:
            ans = player.plr_choose_options(
                "Play another cultist?",
                ("Don't play cultist", False),
                ("Play another cultist", True),
            )
            if ans:
                player.play_card(cultist, costAction=False)

    def hook_trashThisCard(self, game, player):
        """When you trash this, +3 cards"""
        player.pickup_cards(3)


###############################################################################
class Test_Cultist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Cultist", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Cultist"].remove()

    def test_play(self):
        """Play a cultists - should give 2 cards"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertEqual(self.victim.discardpile.size(), 1)
        self.assertTrue(self.victim.discardpile[0].isRuin())

    def test_defense(self):
        """Make sure moats work against cultists"""
        self.plr.add_card(self.card, "hand")
        moat = self.g["Moat"].remove()
        self.victim.add_card(moat, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertTrue(self.victim.discardpile.is_empty())

    def test_noother(self):
        """Don't ask to play another cultist if it doesn't exist"""
        self.plr.hand.set("Estate", "Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.test_input, ["0"])

    def test_anothercultist_no(self):
        """Don't play the other cultist"""
        self.plr.hand.set("Cultist", "Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.played.size(), 1)

    def test_anothercultist_yes(self):
        """Another cultist can be played for free"""
        self.plr.hand.set("Cultist", "Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.played.size(), 2)
        self.assertEqual(self.plr.get_actions(), 0)
        for c in self.plr.played:
            self.assertEqual(c.name, "Cultist")
        self.assertEqual(self.victim.discardpile.size(), 2)
        for c in self.victim.discardpile:
            self.assertTrue(c.isRuin())

    def test_trash(self):
        """Trashing a cultist should give 3 more cards"""
        self.plr.add_card(self.card, "hand")
        self.plr.trash_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Cultist"))
        self.assertEqual(self.plr.hand.size(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
