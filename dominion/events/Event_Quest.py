#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Quest"""
import unittest

from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Quest(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Discard stuff to gain a gold"
        self.name = "Quest"
        self.cost = 0

    def special(self, game, player):
        """You may discard an attack, two curses or six cards. If you do, gain a gold"""
        player.output("Discard any number of cards")
        player.output(
            "If you discard an Attack Card or Two Curses or Six Cards you gain a Gold"
        )
        discards = player.plr_discard_cards(any_number=True)
        attack_flag = False
        curses = 0
        if not discards:
            return
        for card in discards:
            if card.isAttack():
                attack_flag = True
            if card.name == "Curse":
                curses += 1
        if len(discards) >= 6 or attack_flag or curses >= 2:
            player.gain_card("Gold")


###############################################################################
class TestQuest(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Quest"], initcards=["Witch"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Quest"]

    def test_with_attack(self):
        """Use Quest with an attack card"""
        self.plr.piles[Piles.HAND].set("Witch")
        self.plr.test_input = ["witch", "finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Witch"])

    def test_with_curses(self):
        """Use Quest with two curse cards"""
        self.plr.piles[Piles.HAND].set("Curse", "Curse")
        self.plr.test_input = ["1", "2", "finish"]
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Curse"])
        self.assertEqual(
            self.plr.piles[Piles.DISCARD].size(), 3
        )  # Two curses + gained gold

    def test_with_six_cards(self):
        """Use Quest with six cards"""
        self.plr.piles[Piles.HAND].set(
            "Copper", "Copper", "Copper", "Copper", "Copper", "Copper"
        )
        self.plr.test_input = ["1", "2", "3", "4", "5", "6", "finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 7)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Copper"])

    def xtest_with_five_cards(self):
        """Use Quest with five cards"""
        self.plr.piles[Piles.HAND].set(
            "Copper", "Copper", "Copper", "Copper", "Copper", "Copper"
        )
        self.plr.test_input = ["1", "2", "3", "4", "5", "finish"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 5)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
