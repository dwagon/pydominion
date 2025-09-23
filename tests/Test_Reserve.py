#!/usr/bin/env python

import unittest

from dominion import Game, Piles, Whens, Phase, Prompt, Action


###############################################################################
class TestGetWhens(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"], badcards=["Pixie"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_start(self) -> None:
        self.plr.start_turn()
        whens = self.plr._get_whens()
        self.assertEqual(whens, ["any", "start"])

    def test_not_start(self) -> None:
        self.plr.start_turn()
        self.plr._perform_action({"action": Action.SPENDALL})
        whens = self.plr._get_whens()
        self.assertNotIn(Whens.START, whens)

    def test_any(self) -> None:
        whens = self.plr._get_whens()
        self.assertIn(Whens.ANY, whens)

    def test_post_action(self) -> None:
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr.phase = Phase.ACTION
        whens = self.plr._get_whens()
        self.assertIn(Whens.POSTACTION, whens)
        self.plr.piles[Piles.PLAYED].set("Copper")
        whens = self.plr._get_whens()
        self.assertNotIn(Whens.POSTACTION, whens)

    def test_not_post_action(self) -> None:
        self.plr.phase = Phase.ACTION
        whens = self.plr._get_whens()
        self.assertNotIn(Whens.POSTACTION, whens)
        self.plr._perform_action({"action": Action.SPENDALL})
        whens = self.plr._get_whens()
        self.assertNotIn(Whens.POSTACTION, whens)


###############################################################################
class TestReserve(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_reserve(self) -> None:
        """Test reserve[]"""
        self.plr.piles[Piles.RESERVE].set("Copper")
        self.assertTrue(self.plr.piles[Piles.RESERVE]["Copper"])
        self.assertEqual(self.plr.piles[Piles.RESERVE]["Copper"].name, "Copper")

    def test_not_reserve(self) -> None:
        """Test reserve[]"""
        self.plr.piles[Piles.RESERVE].set("Copper")
        self.assertFalse(self.plr.piles[Piles.RESERVE]["Estate"])

    def test_reserve_set(self) -> None:
        """set reserved"""
        self.plr.piles[Piles.RESERVE].set("Silver")
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 1)
        self.assertEqual(self.plr.piles[Piles.RESERVE][0].name, "Silver")

    def test_call_reserve(self) -> None:
        self.plr.piles[Piles.RESERVE].set("Silver")
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 1)
        c = self.plr.call_reserve("Silver")
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 0)
        self.assertEqual(c.name, "Silver")

    def test_bad_call_reserve(self) -> None:
        """Call a reserve that isn't there!"""
        self.plr.piles[Piles.RESERVE].set("Copper")
        c = self.plr.call_reserve("Silver")
        self.assertIsNone(c)

    def test_addcard_reserve(self) -> None:
        gold = self.g.get_card_from_pile("Gold")
        self.plr.add_card(gold, Piles.RESERVE)
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 1)
        self.assertEqual(self.plr.piles[Piles.RESERVE][0].name, "Gold")

    def test_isreserve(self) -> None:
        gold = self.g.get_card_from_pile("Gold")
        self.assertFalse(gold.isReserve())
        cotr = self.g.get_card_from_pile("Coin of the Realm")
        self.assertTrue(cotr.isReserve())


###############################################################################
class Test_reserveSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_callable(self) -> None:
        gold = self.g.get_card_from_pile("Gold")
        self.plr.add_card(gold, Piles.RESERVE)
        output, index = Prompt.reserve_selection(self.plr, 1)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["action"], Action.RESERVE)
        self.assertEqual(output[0]["card"], gold)
        self.assertEqual(output[0]["selector"], "c")
        self.assertEqual(index, 2)

    def test_not_callable(self) -> None:
        """Copper is not callable (Due to miser)"""
        copper = self.g.get_card_from_pile("Copper")
        self.plr.add_card(copper, Piles.RESERVE)
        output, index = Prompt.reserve_selection(self.plr, 1)
        self.assertEqual(len(output), 0)
        self.assertEqual(index, 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
