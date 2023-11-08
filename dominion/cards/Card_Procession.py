#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Procession(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """You may play a non-Duration Action card from your
            hand twice. Trash it. Gain an Action
            card costing exactly 1 more than it."""
        self.name = "Procession"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        action_cards = [
            _ for _ in player.piles[Piles.HAND] if _.isAction() and not _.isDuration()
        ]
        if not action_cards:
            player.output("No suitable action cards")
            return
        cards = player.card_sel(
            prompt="Select a card to play twice, then trash", cardsrc=action_cards
        )
        if not cards:
            return
        card = cards[0]
        player.move_card(card, Piles.PLAYED)

        for i in range(1, 3):
            player.output(f"Play {i} of {card}")
            player.play_card(card, discard=False, cost_action=False)
        player.trash_card(card)
        cost = player.card_cost(card) + 1
        player.plr_gain_card(cost, modifier="equal", types={Card.CardType.ACTION: True})


###############################################################################
class TestProcession(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Procession", "Moat", "Witch"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Procession")

    def test_play(self) -> None:
        """Play procession to trash moat and buy a witch"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Moat", "Witch"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)
        self.assertIn("Witch", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
