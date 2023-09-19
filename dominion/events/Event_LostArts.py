#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Lost_Arts"""
import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_LostArts(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Move your +1 Action Token to an Action Supply Pile"
        self.name = "Lost Arts"
        self.cost = 6

    def special(self, game, player):
        """Move your +1 Action token to an Action Supply Pile"""
        stacks = player.card_pile_sel(
            num=1,
            prompt="What stack to add the +1 Action Token to?",
            cardsrc=game.get_action_piles(),
        )
        if stacks:
            player.place_token("+1 Action", stacks[0])


###############################################################################
class TestLostArts(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, eventcards=["Lost Arts"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Lost Arts"]

    def test_with_treasure(self):
        """Use Lost Arts"""
        self.plr.coins.add(6)
        self.plr.test_input = ["moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.tokens["+1 Action"], "Moat")
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
