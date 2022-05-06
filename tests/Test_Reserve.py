#!/usr/bin/env python

import unittest
from dominion import Game


###############################################################################
class Test__get_whens(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"], badcards=["Pixie"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_start(self):
        self.plr.start_turn()
        whens = self.plr._get_whens()
        self.assertEqual(whens, ["any", "start"])

    def test_not_start(self):
        self.plr.start_turn()
        self.plr._perform_action({"action": "spendall"})
        whens = self.plr._get_whens()
        self.assertNotIn("start", whens)

    def test_any(self):
        whens = self.plr._get_whens()
        self.assertIn("any", whens)

    def test_postaction(self):
        self.plr.played.set("Moat")
        whens = self.plr._get_whens()
        self.assertIn("postaction", whens)
        self.plr.played.set("Copper")
        whens = self.plr._get_whens()
        self.assertNotIn("postaction", whens)

    def test_not_postaction(self):
        whens = self.plr._get_whens()
        self.assertNotIn("postaction", whens)
        self.plr._perform_action({"action": "spendall"})
        whens = self.plr._get_whens()
        self.assertNotIn("postaction", whens)


###############################################################################
class Test_Reserve(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_reserve(self):
        """Test reserve[]"""
        self.plr.reserve.set("Copper")
        self.assertTrue(self.plr.reserve["Copper"])
        self.assertEqual(self.plr.reserve["Copper"].name, "Copper")

    def test_not_reserve(self):
        """Test reserve[]"""
        self.plr.reserve.set("Copper")
        self.assertFalse(self.plr.reserve["Estate"])

    def test_reserve_set(self):
        """set reserved"""
        self.plr.reserve.set("Silver")
        self.assertEqual(self.plr.reserve.size(), 1)
        self.assertEqual(self.plr.reserve[0].name, "Silver")

    def test_call_reserve(self):
        self.plr.reserve.set("Silver")
        self.assertEqual(self.plr.reserve.size(), 1)
        c = self.plr.call_reserve("Silver")
        self.assertEqual(self.plr.reserve.size(), 0)
        self.assertEqual(c.name, "Silver")

    def test_bad_call_reserve(self):
        """Call a reserve that isn't there!"""
        self.plr.reserve.set("Copper")
        c = self.plr.call_reserve("Silver")
        self.assertIsNone(c)

    def test_addcard_reserve(self):
        gold = self.g["Gold"].remove()
        self.plr.add_card(gold, "reserve")
        self.assertEqual(self.plr.reserve.size(), 1)
        self.assertEqual(self.plr.reserve[0].name, "Gold")

    def test_isreserve(self):
        gold = self.g["Gold"].remove()
        self.assertFalse(gold.isReserve())
        cotr = self.g["Coin of the Realm"].remove()
        self.assertTrue(cotr.isReserve())


###############################################################################
class Test_reserveSelection(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_callable(self):
        gold = self.g["Gold"].remove()
        self.plr.add_card(gold, "reserve")
        output, index = self.plr._reserve_selection(1)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["action"], "reserve")
        self.assertEqual(output[0]["card"], gold)
        self.assertEqual(output[0]["selector"], "c")
        self.assertEqual(index, 2)

    def test_not_callable(self):
        """Copper is not callable (Due to miser)"""
        copper = self.g["Copper"].remove()
        self.plr.add_card(copper, "reserve")
        output, index = self.plr._reserve_selection(1)
        self.assertEqual(len(output), 0)
        self.assertEqual(index, 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
