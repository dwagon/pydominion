#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/March"""
import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_March(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "March"
        self.desc = (
            """ Look through your discard pile. You may play an Action card from it."""
        )
        self.cost = 3

    def special(self, game, player):
        """You may play an Action card from it."""
        options = []
        for card in player.piles[Piles.DISCARD]:
            if card.isAction():
                options.append((f"Play {card}", card))
        if not options:
            player.output("No applicable cards")
            return
        options.insert(0, ("Play nothing", None))
        play = player.plr_choose_options(
            "March: Play a card from the discard pile", *options
        )
        if play:
            player.play_card(play, cost_action=False, discard=False)


###############################################################################
class TestMarch(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["March"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["March"]

    def test_with_treasure(self):
        """Use March with actions"""
        self.plr.coins.set(3)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.piles[Piles.DISCARD].set("Estate", "Moat", "Copper")
        self.plr.test_input = ["Play Moat"]
        self.plr.perform_event(self.card)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2)  # Moat


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
