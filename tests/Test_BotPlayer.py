#!/usr/bin/env python

import unittest

from dominion import Game, Piles


###############################################################################
class TestGetOptions(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, bot=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_getOptions(self):
        options = [
            {"action": "quit", "verb": "End Phase", "selector": "0", "card": None},
            {
                "action": "buy",
                "desc": "+1 coin",
                "selector": "-",
                "card": self.g.get_card_from_pile("Copper"),
                "name": "Copper",
                "details": "0 Coins; Treasure; 60 left",
                "verb": "",
            },
            {
                "action": "buy",
                "desc": "1 VP",
                "selector": "-",
                "card": self.g.get_card_from_pile("Estate"),
                "name": "Estate",
                "details": "2 Coins; Victory; 12 left",
                "verb": "",
            },
            {
                "action": "buy",
                "desc": "+2 coin",
                "selector": "-",
                "card": self.g.get_card_from_pile("Silver"),
                "name": "Silver",
                "details": "3 Coins; Treasure; 39 left",
                "verb": "",
            },
            {
                "action": None,
                "desc": "3 VP",
                "selector": "-",
                "card": self.g.get_card_from_pile("Duchy"),
                "name": "Duchy",
                "details": "5 Coins; Victory; 12 left",
                "verb": "",
            },
            {
                "action": "buy",
                "desc": "+3 coin",
                "selector": "-",
                "card": self.g.get_card_from_pile("Gold"),
                "name": "Gold",
                "details": "6 Coins; Treasure; 30 left",
                "verb": "",
            },
            {
                "action": "buy",
                "desc": "6 VP",
                "selector": "-",
                "card": self.g.get_card_from_pile("Province"),
                "name": "Province",
                "details": "8 Coins; Victory; 12 left",
                "verb": "",
            },
            {"action": "quit", "card": None, "verb": "End Phase", "selector": "0"},
        ]
        ans = self.plr.get_options(options)
        self.assertEqual(ans["silver"]["name"], "Silver")
        self.assertEqual(ans["gold"]["name"], "Gold")
        self.assertEqual(ans["quit"]["verb"], "End Phase")
        self.assertNotIn("duchy", ans)


###############################################################################
class TestPickToDiscard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, bot=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_no_discard(self):
        """Test pick_to_discard with no discard requirement"""
        self.plr.piles[Piles.HAND].set("Estate", "Copper", "Copper", "Gold")
        card = self.plr.pick_to_discard(0)
        self.assertEqual(len(card), 0)

    def test_not_treasure(self):
        """Test pick_to_discard with a non-treasure to discard"""
        self.plr.piles[Piles.HAND].set("Estate", "Copper", "Copper", "Gold")
        card = self.plr.pick_to_discard(1)
        self.assertEqual(len(card), 1)
        self.assertEqual(card[0].name, "Estate")

    def test_treasure(self):
        """Test pick_to_discard when it has to drop a treasure"""
        self.plr.piles[Piles.HAND].set("Estate", "Copper", "Silver", "Gold")
        cards = self.plr.pick_to_discard(2)
        self.assertEqual(len(cards), 2)
        cardnames = [c.name for c in cards]

        self.assertIn("Estate", cardnames)
        self.assertIn("Copper", cardnames)

    def test_good_treasure(self):
        """Test pick_to_discard when it has to drop good treasures"""
        self.plr.piles[Piles.HAND].set("Gold", "Gold", "Silver", "Gold")
        cards = self.plr.pick_to_discard(2)
        self.assertEqual(len(cards), 2)
        cardnames = [_.name for _ in cards]

        self.assertIn("Silver", cardnames)
        self.assertIn("Gold", cardnames)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
