#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Peril"""
import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Peril(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.name = "Peril"
        self.cost = 2
        self.desc = """You may trash an Action card from your hand to gain a Loot."""
        self.required_cards = ["Loot"]

    def special(self, game, player):
        """You may trash an Action card from your hand to gain a Loot."""
        actions = [(f"Trash {_}", _) for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            player.output("No suitable cards")
            return
        actions.insert(0, ("Trash nothing", None))
        to_trash = player.plr_choose_options("Trash a card to gain a Loot", *actions)
        if to_trash:
            player.trash_card(to_trash)
            player.gain_card("Loot")


###############################################################################
class Test_Peril(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Peril"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Peril"]

    def test_play(self):
        """Use Peril"""
        self.plr.coins.set(2)
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Trash Moat"]
        self.plr.perform_event(self.card)
        self.assertIn("Moat", self.g.trash_pile)
        found = any([True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot()])
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
