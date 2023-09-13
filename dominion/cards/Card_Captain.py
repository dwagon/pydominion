#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Captain(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.REACTION,
            Card.CardType.COMMAND,
        ]
        self.base = Card.CardExpansion.PROMO
        self.desc = """Now and at the start of your next turn:
            Play a non-Duration, non-Command Action card from the Supply costing
            up to 4 Coin, leaving it there."""
        self.name = "Captain"
        self.cost = 6

    def special(self, game, player):
        self.special_sauce(game, player)

    def duration(self, game, player):
        self.special_sauce(game, player)

    def special_sauce(self, game, player):
        options = [("None", None)]
        for name in game.getActionPiles(4):
            card = game.get_card_from_pile(name)
            if card.isDuration():
                continue
            if card.isCommand():
                continue
            options.append((f"Play {name}", card))

        action = player.plr_choose_options(
            "What action card do you want to imitate?", *options
        )
        if action:
            player.card_benefits(action)


###############################################################################
class TestCaptain(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Captain", "Workshop", "Bureaucrat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Captain"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_bureaucrat(self):
        """Make the Captain be a Bureaucrat"""
        self.plr.test_input = ["Bureaucrat"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])

    def test_play_market(self):
        """Make the Captain be a Workshop"""
        self.plr.test_input = ["Play Workshop", "Get Bureaucrat"]
        self.plr.play_card(self.card)
        self.assertNotIn("Workshop", self.plr.piles[Piles.DISCARD])
        self.assertIn("Bureaucrat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
