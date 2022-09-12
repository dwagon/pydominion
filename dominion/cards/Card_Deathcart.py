#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Deathcart(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LOOTER]
        self.base = Game.DARKAGES
        self.desc = """You may trash this or an Action card from your hand, for +5 Coin.
            When you gain this, gain 2 Ruins."""
        self.name = "Death Cart"
        self.cost = 4

    def special(self, game, player):
        action_cards = [c for c in player.hand if c.isAction()]
        choices = [
            ("Trash this Death Cart for 5 Gold", "trash_dc"),
        ]
        if action_cards:
            choices.append(("Trash an Action card for 5 Gold", "trash_action"))
        else:
            choices.append(("No action cards to trash", "nothing"))
        choices.append(("Do nothing", "nothing"))
        ans = player.plr_choose_options("What to do with Death Cart?", *choices)
        trash = None
        if ans == "nothing":
            return
        if ans == "trash_action":
            trash = player.plr_trash_card(cardsrc=action_cards)
        if ans == "trash_dc":
            player.output("Trashing Death Cart")
            player.trash_card(self)
            trash = True
        if trash:
            player.coins.add(5)

    def hook_gain_this_card(self, game, player):
        for _ in range(2):
            c = player.gain_card("Ruins")
            player.output(f"Gained {c.name}")
        return {}


###############################################################################
class Test_Deathcart(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Death Cart", "Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Death Cart"].remove()

    def test_play(self):
        """Play a death cart - no actions"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Do nothing"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertNotIn("Death Cart", self.g.trashpile)

    def test_play_trash_action(self):
        """Play a death cart - no actions"""
        self.plr.hand.set("Copper", "Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash an Action", "Trash Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertIn("Moat", self.g.trashpile)
        self.assertNotIn("Death Cart", self.g.trashpile)

    def test_play_trash_self(self):
        """Play a death cart - no actions"""
        self.plr.hand.set("Copper", "Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash this Death"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertNotIn("Moat", self.g.trashpile)
        self.assertIn("Death Cart", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
