#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Cultist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.LOOTER,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 Cards; Each other player gains a Ruins. You may play
            a Cultist from your hand.  When you trash this, +3 Cards."""
        self.name = "Cultist"
        self.cost = 5
        self.cards = 2

    def special(self, game, player):
        """Each other play gains a Ruins. You may play a Cultist
        from your hand."""
        for plr in player.attack_victims():
            plr.output(f"Gained a ruin from {player.name}'s Cultist")
            plr.gain_card("Ruins")
        cultist = player.piles[Piles.HAND]["Cultist"]
        if cultist:
            ans = player.plr_choose_options(
                "Play another cultist?",
                ("Don't play cultist", False),
                ("Play another cultist", True),
            )
            if ans:
                player.play_card(cultist, cost_action=False)

    def hook_trashThisCard(self, game, player):
        """When you trash this, +3 cards"""
        player.pickup_cards(3)


###############################################################################
class TestCultist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Cultist", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Cultist")

    def test_play(self):
        """Play a cultists - should give 2 cards"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 1)
        print(f"card = {self.victim.piles[Piles.DISCARD][0]}")
        self.assertTrue(self.victim.piles[Piles.DISCARD][0].isRuin())

    def test_defense(self):
        """Make sure moats work against cultists"""
        self.plr.add_card(self.card, Piles.HAND)
        moat = self.g.get_card_from_pile("Moat")
        self.victim.add_card(moat, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())

    def test_no_other(self):
        """Don't ask to play another cultist if it doesn't exist"""
        self.plr.piles[Piles.HAND].set("Estate", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.test_input, ["0"])

    def test_another_cultist_no(self):
        """Don't play the other cultist"""
        self.plr.piles[Piles.HAND].set("Cultist", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)

    def test_another_cultist_yes(self):
        """Another cultist can be played for free"""
        self.plr.piles[Piles.HAND].set("Cultist", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 2)
        self.assertEqual(self.plr.actions.get(), 0)
        for c in self.plr.piles[Piles.PLAYED]:
            self.assertEqual(c.name, "Cultist")
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)
        for c in self.victim.piles[Piles.DISCARD]:
            self.assertTrue(c.isRuin())

    def test_trash(self):
        """Trashing a cultist should give 3 more cards"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.trash_card(self.card)
        self.assertIn("Cultist", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
