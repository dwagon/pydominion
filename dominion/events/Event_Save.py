#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event, PlayArea


###############################################################################
class Event_Save(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Buy. Once per turn: Set aside a card from your hand, and put it into your hand at end of turn (after drawing)."
        self.name = "Save"
        self.cost = 1

    def special(self, game, player):
        if not player.do_once("Save"):
            player.output("Already used save this turn")
            return
        if player.piles[Piles.HAND].is_empty():
            player.output("No cards in hand")
            return
        card = player.card_sel(
            num=1,
            cardsrc=Piles.HAND,
            verbs=("Set", "Unset"),
            prompt=" Set aside a card from your hand, and put it into your hand at end of turn",
        )
        player._save_reserve = PlayArea.PlayArea([])
        player._save_reserve.add(card[0])
        player.piles[Piles.HAND].remove(card[0])
        player.secret_count += 1

    def hook_end_turn(self, game, player):
        if not hasattr(player, "_save_reserve") or len(player._save_reserve) == 0:
            return
        card = player._save_reserve[0]
        player.add_card(card, Piles.HAND)
        player.secret_count -= 1
        del player._save_reserve


###############################################################################
class TestSave(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Save"], initcards=["Militia"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Save"]

    def test_play(self):
        """Use Save"""
        self.plr.coins.set(1)
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.test_input = ["Gold"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr._save_reserve[0].name, "Gold")
        self.plr.end_turn()
        self.assertIn("Gold", self.plr.piles[Piles.HAND])

    def test_empty_hand(self):
        """Use a save when there are no cards in your hand"""
        self.plr.coins.set(1)
        self.plr.piles[Piles.HAND].empty()
        self.plr.perform_event(self.card)
        self.plr.end_turn()
        self.g.print_state()
        self.assertEqual(5, len(self.plr.piles[Piles.HAND]))  # Just the hands dealt


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
