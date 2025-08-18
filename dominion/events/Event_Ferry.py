#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Ferry"""
import unittest

from dominion import Card, Game, Event, Token


###############################################################################
class Event_Ferry(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Move your -2 Coin token to an Action Supply pile."
        self.name = "Ferry"
        self.cost = 3

    def special(self, game, player):
        action_piles = game.get_action_piles()
        piles = player.card_pile_sel(
            num=1,
            prompt="What stack to add the -2 Coin Token to?",
            cardsrc=action_piles,
        )
        if piles:
            player.place_token(Token.MINUS_2_COST, piles[0])


###############################################################################
class TestFerry(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Ferry"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Ferry"]

    def test_play(self):
        self.plr.coins.add(3)
        self.plr.test_input = ["moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.tokens[Token.MINUS_2_COST], "Moat")
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
