#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Captain(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION, Card.TYPE_COMMAND]
        self.base = Game.PROMO
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
        actionpiles = [
            _
            for _ in game.getActionPiles(4)
            if not _.isDuration() and not _.isCommand()
        ]
        actions = player.card_sel(
            prompt="What action card do you want to imitate?", cardsrc=actionpiles
        )
        if actions:
            player.card_benefits(actions[0])


###############################################################################
class Test_Captain(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Captain", "Workshop", "Bureaucrat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Captain"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_bureaucrat(self):
        """Make the Captain be a Bureaucrat"""
        self.plr.test_input = ["Bureaucrat"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_deck("Silver"))

    def test_play_market(self):
        """Make the Captain be a Workshop"""
        self.plr.test_input = ["Select Workshop", "Get Bureaucrat"]
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.in_discard("Workshop"))
        self.assertIsNotNone(self.plr.in_discard("Bureaucrat"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
