#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Hamlet(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+1 Card +1 Action. You may discard a card; if you do, +1 Action.
                You may discard a card; if you do, +1 Buy."""
        self.name = "Hamlet"
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if player.plr_discard_cards(prompt="Discard a card to gain an action"):
            player.add_actions(1)
        if player.plr_discard_cards(prompt="Discard card to gain a buy"):
            player.buys.add(1)


###############################################################################
class Test_Hamlet(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Hamlet"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Hamlet")
        self.plr.piles[Piles.HAND].set("Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self) -> None:
        """Play a hamlet"""
        self.plr.test_input = ["finish selecting", "finish selecting"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_discard_action(self) -> None:
        """Play a hamlet and discard to gain an action"""
        self.plr.test_input = ["discard silver", "finish selecting"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertNotIn("Silver", self.plr.piles[Piles.HAND])

    def test_discard_buy(self) -> None:
        """Play a hamlet and discard to gain a buy"""
        self.plr.test_input = ["finish selecting", "discard gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
