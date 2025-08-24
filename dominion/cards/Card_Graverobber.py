#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles


###############################################################################
class Card_Graverobber(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Choose one: Gain a card from the trash costing from 3 to 6,
            putting it on top of your deck; or trash an Action card from your hand
            and gain a card costing up to 3 more than it."""
        self.name = "Graverobber"
        self.cost = 5

    def special(self, game, player):
        trash = player.plr_choose_options(
            "Pick one",
            (
                "Gain a card from the trash costing from 3 to 6 putting it on top of your deck",
                False,
            ),
            (
                "Trash an Action card from your hand and gain a card costing up to 3 more",
                True,
            ),
        )
        if trash:
            actions = [c for c in player.piles[Piles.HAND] if c.isAction()]
            if not actions:
                player.output("No suitable action cards")
                return
            card = player.plr_trash_card(cardsrc=actions)
            player.plr_gain_card(cost=card[0].cost + 3)
        else:
            trash_cards = [c for c in game.trash_pile if 3 <= c.cost <= 6]
            if not trash_cards:
                player.output("No suitable cards in trash")
                return
            if cards := player.card_sel(cardsrc=trash_cards):
                card = cards[0]
                game.trash_pile.remove(card)
                player.add_card(card, Piles.TOPDECK)


###############################################################################
class Test_Graverobber(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Graverobber", "Militia"],
            badcards=["Fool's Gold", "Gold Mine"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Graverobber")
        self.plr.add_card(self.card, Piles.HAND)

    def test_trash(self):
        """Play a grave robber - trash a militia and gain a gold"""
        militia = self.g.get_card_from_pile("Militia")
        self.plr.add_card(militia, Piles.HAND)
        self.plr.test_input = ["1", "militia", "get gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Militia", self.plr.piles[Piles.HAND])

    def test_trash_empty(self):
        """Play a grave robber - nothing to trash"""
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)

    def test_loot(self):
        """Play a grave robber - looting the trash"""
        self.g.trash_pile.set("Militia")
        self.plr.test_input = ["0", "militia"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), 0)
        self.assertIn("Militia", self.plr.piles[Piles.DECK])

    def test_loot_empty(self):
        """Play a grave robber - looting the trash that doesn't have anything"""
        self.g.trash_pile.set("Copper")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
