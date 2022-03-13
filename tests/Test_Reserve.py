#!/usr/bin/env python

import unittest
from dominion import Game


###############################################################################
class Test_getWhens(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Moat"], badcards=["Pixie"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_start(self):
        self.plr.start_turn()
        whens = self.plr.getWhens()
        self.assertEqual(whens, ["any", "start"])

    def test_not_start(self):
        self.plr.start_turn()
        self.plr.perform_action({"action": "spendall"})
        whens = self.plr.getWhens()
        self.assertNotIn("start", whens)

    def test_any(self):
        whens = self.plr.getWhens()
        self.assertIn("any", whens)

    def test_postaction(self):
        self.plr.setPlayed("Moat")
        whens = self.plr.getWhens()
        self.assertIn("postaction", whens)
        self.plr.setPlayed("Copper")
        whens = self.plr.getWhens()
        self.assertNotIn("postaction", whens)

    def test_not_postaction(self):
        whens = self.plr.getWhens()
        self.assertNotIn("postaction", whens)
        self.plr.perform_action({"action": "spendall"})
        whens = self.plr.getWhens()
        self.assertNotIn("postaction", whens)


###############################################################################
class Test_Reserve(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_inreserve(self):
        """Test in_reserve()"""
        self.plr.set_reserve("Copper")
        self.assertTrue(self.plr.in_reserve("Copper"))
        self.assertEqual(self.plr.in_reserve("Copper").name, "Copper")

    def test_not_inreserve(self):
        """Test in_reserve()"""
        self.plr.set_reserve("Copper")
        self.assertFalse(self.plr.in_reserve("Estate"))

    def test_set_reserve(self):
        """set reserved"""
        self.plr.set_reserve("Silver")
        self.assertEqual(self.plr.reserve.size(), 1)
        self.assertEqual(self.plr.reserve[0].name, "Silver")

    def test_call_reserve(self):
        self.plr.set_reserve("Silver")
        self.assertEqual(self.plr.reserve.size(), 1)
        c = self.plr.call_reserve("Silver")
        self.assertEqual(self.plr.reserve.size(), 0)
        self.assertEqual(c.name, "Silver")

    def test_bad_call_reserve(self):
        """Call a reserve that isn't there!"""
        self.plr.set_reserve("Copper")
        c = self.plr.call_reserve("Silver")
        self.assertIsNone(c)

    def test_addcard_reserve(self):
        gold = self.g["Gold"].remove()
        self.plr.addCard(gold, "reserve")
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_callable(self):
        gold = self.g["Gold"].remove()
        self.plr.addCard(gold, "reserve")
        output, index = self.plr.reserve_selection(1)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["action"], "reserve")
        self.assertEqual(output[0]["card"], gold)
        self.assertEqual(output[0]["selector"], "c")
        self.assertEqual(index, 2)

    def test_not_callable(self):
        """Copper is not callable (Due to miser)"""
        copper = self.g["Copper"].remove()
        self.plr.addCard(copper, "reserve")
        output, index = self.plr.reserve_selection(1)
        self.assertEqual(len(output), 0)
        self.assertEqual(index, 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
