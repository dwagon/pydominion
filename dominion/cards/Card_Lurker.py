#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Lurker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+1 Action; Choose one: Trash an Action card from the Supply, or gain an Action card from the trash."
        self.name = "Lurker"
        self.cost = 2
        self.actions = 1

    def special(self, game, player):
        ch = player.plr_choose_options(
            "Choose one? ",
            ("Trash an Action from the Supply", "to"),
            ("Gain an Action card from the Trash", "from"),
        )
        if ch == "to":
            self._trash_supply(game, player)
        if ch == "from":
            self._from_trash(game, player)

    def _trash_supply(self, game, player):
        """Trash an action from supply"""
        options = []
        for name, pile in game.card_piles():
            if pile.is_empty():
                continue
            card = game.get_card_from_pile(name)
            if card.isAction():
                options.append((f"Trash {name}", name))

        if not options:
            player.output("No suitable cards found")
            return
        to_trash = player.plr_choose_options(
            "Select Action from Supply to Trash", *options
        )
        card = game.get_card_from_pile(to_trash)
        player.add_card(card, "played")  # In order to trash
        player.trash_card(card)

    def _from_trash(self, game, player):
        """Gain an action from the trash"""
        acts = [_ for _ in game.trash_pile if _.isAction()]
        if not acts:
            player.output("No suitable cards found")
            return
        card = player.card_sel(cardsrc=acts, prompt="Select Action from the Trash")
        game.trash_pile.remove(card[0])
        player.add_card(card[0], "discard")


###############################################################################
class TestLurker(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Lurker", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Lurker"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_trash(self):
        self.plr.test_input = ["Trash an Action", "Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.g.trash_pile)
        self.assertEqual(self.plr.actions.get(), 0 + 1)

    def test_recover(self):
        self.plr.test_input = ["Gain an Action", "Moat"]
        self.g.trash_pile.set("Moat")
        self.plr.play_card(self.card)
        self.assertNotIn("Moat", self.g.trash_pile)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
