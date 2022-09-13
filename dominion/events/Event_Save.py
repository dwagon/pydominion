#!/usr/bin/env python

import unittest
from dominion import Game, Event, PlayArea


###############################################################################
class Event_Save(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "+1 Buy. Once per turn: Set aside a card from your hand, and put it into your hand at end of turn (after drawing)."
        self.name = "Save"
        self.cost = 1

    def special(self, game, player):
        if not player.do_once("Save"):
            player.output("Already used save this turn")
            return
        player._save_reserve = PlayArea.PlayArea([])
        card = player.card_sel(
            num=1,
            cardsrc="hand",
            verbs=("Set", "Unset"),
            prompt=" Set aside a card from your hand, and put it into your hand at end of turn",
        )
        player._save_reserve.add(card[0])
        player.hand.remove(card[0])
        player.secret_count += 1

    def hook_end_turn(self, game, player):
        card = player._save_reserve[0]
        player.add_card(card, "hand")
        player.secret_count -= 1
        del player._save_reserve


###############################################################################
class Test_Save(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Save"], initcards=["Militia"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Save"]

    def test_play(self):
        """Use Save"""
        self.plr.coins.set(1)
        self.plr.hand.set("Gold")
        self.plr.test_input = ["Gold"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr._save_reserve[0].name, "Gold")
        self.plr.end_turn()
        self.assertIn("Gold", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
