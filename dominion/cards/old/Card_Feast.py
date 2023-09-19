#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Feast(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Trash this card, Gain a card costing up to 5"
        self.name = "Feast"
        self.cost = 4

    def special(self, game, player):
        """Trash this card. Gain a card costing up to 5"""
        if self.trash_card(player):
            self.selectNewCard(game, player)

    def selectNewCard(self, game, player):
        player.output("Gain a card costing up to 5")
        options = [{"selector": "0", "print": "Nothing", "card": None}]
        buyable = player.cards_under(5)
        index = 1
        for p in buyable:
            to_print = "Get %s (%d coin)" % (p.name, p.cost)
            options.append({"selector": f"{index}", "print": to_print, "card": p})
            index += 1

        o = player.user_input(options, "What card do you wish?")
        if o["card"]:
            player.gain_card(o["card"].name)
            player.output(f"Took {o['card']}")

    def trash_card(self, player):
        ans = player.plr_choose_options(
            "Trash this card?", ("Keep this card", False), ("Trash this card", True)
        )
        if ans:
            player.trash_card(self)
            return True
        return False


###############################################################################
class TestFeast(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Feast"],
            oldcards=True,
            badcards=["Den of Sin", "Ghost Town", "Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Feast"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_dontTrash(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["keep this"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize)
        try:
            self.assertEqual(self.plr.piles[Piles.PLAYED][0].name, "Feast")
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_trashForNothing(self):
        tsize = self.g.trash_pile.size()
        try:
            self.plr.test_input = ["trash", "nothing"]
            self.plr.play_card(self.card)
            self.assertEqual(self.g.trash_pile.size(), tsize + 1)
            self.assertIn("Feast", self.g.trash_pile)
            self.assertTrue(self.plr.piles[Piles.PLAYED].is_empty())
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_trashForSomething(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["trash", "Get Duchy"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.g.trash_pile.size(), tsize + 1)
            self.assertIn("Feast", self.g.trash_pile)
            self.assertTrue(self.plr.piles[Piles.PLAYED].is_empty())
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
            self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Duchy"])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
