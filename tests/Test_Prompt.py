#!/usr/bin/env python
# pylint: disable=protected-access
"""Testing prompt code"""

import operator
import unittest

from dominion import Card, Game, Phase, Piles, Prompt
from dominion.Counter import Counter


###############################################################################
class TestCardsAffordable(unittest.TestCase):
    """Test the cards_affordable functionality"""

    def setUp(self) -> None:
        self.game = Game.TestGame(
            numplayers=1,
            badcards=[
                "Werewolf",
                "Cursed Village",
                "Leprechaun",
                "Skulk",
                "Tormentor",
                "Vampire",
                "Bridge Troll",
                "Highway",
                "Fisherman",
                "Souk",
            ],
        )
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_under(self) -> None:
        """Test cards under a cost"""
        price = 4
        ans = self.plr.cards_under(price, types={Card.CardType.ACTION: True})
        for a in ans:
            try:
                self.assertLessEqual(a.cost, price)
                self.assertTrue(a.isAction())
            except AssertionError:  # pragma: no cover
                print(f"Failed on card: {a}")
                self.game.print_state()
                raise

    def test_worth(self) -> None:
        """Test cards equal to a cost"""
        price = 5
        ans = self.plr.cards_worth(price, types={Card.CardType.VICTORY: True})
        for a in ans:
            self.assertEqual(a.cost, price)
            self.assertTrue(a.isVictory())

    def test_over(self) -> None:
        """Test cards over a cost"""
        price = 4
        ans = self.plr.cards_over(price)
        for a in ans:
            self.assertGreater(a.cost, price)
        self.assertIn("Gold", [_.name for _ in ans])

    def test_no_cost(self) -> None:
        """Test with no cost"""
        ans = self.plr.cards_affordable(
            oper=operator.le,
            coin=None,
            num_potions=0,
            types={
                Card.CardType.VICTORY: True,
                Card.CardType.ACTION: True,
                Card.CardType.TREASURE: True,
                Card.CardType.NIGHT: True,
            },
        )
        self.assertIn("Province", [_.name for _ in ans])


###############################################################################
class TestTypeSelector(unittest.TestCase):
    """Test _type_selector()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_select_zero(self) -> None:
        """Test selecting zero types"""
        x = self.plr._type_selector({})
        self.assertTrue(x[Card.CardType.ACTION])
        self.assertTrue(x[Card.CardType.TREASURE])
        self.assertTrue(x[Card.CardType.VICTORY])

    def test_select_one(self) -> None:
        """Test selecting one type"""
        x = self.plr._type_selector({Card.CardType.ACTION: True})
        self.assertTrue(x[Card.CardType.ACTION])
        self.assertFalse(x[Card.CardType.TREASURE])
        self.assertFalse(x[Card.CardType.VICTORY])

    def test_select_two(self) -> None:
        """Test selecting two types"""
        x = self.plr._type_selector({Card.CardType.ACTION: True, Card.CardType.VICTORY: True})
        self.assertTrue(x[Card.CardType.ACTION])
        self.assertFalse(x[Card.CardType.TREASURE])
        self.assertTrue(x[Card.CardType.VICTORY])


###############################################################################
class TestDisplayOverview(unittest.TestCase):
    """Test the display overview at the start of every user input"""

    def setUp(self) -> None:
        self.game = Game.TestGame(
            numplayers=1,
            initcards=["Moat"],
            projects=["Cathedral"],
            landmarks=["Baths"],
        )
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_empty(self) -> None:
        """When we have empty hands"""
        self.plr.messages = []
        self.plr.piles[Piles.HAND].set()
        self.plr.piles[Piles.PLAYED].set()
        Prompt.display_overview(self.plr)
        self.assertIn("| Hand: <EMPTY>", self.plr.messages)
        self.assertIn("| Played: <NONE>", self.plr.messages)

    def test_non_empty(self) -> None:
        """Test not empty hand"""
        self.plr.messages = []
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.piles[Piles.PLAYED].set("Moat")
        Prompt.display_overview(self.plr)
        self.assertIn("| Hand (2): Copper, Estate", self.plr.messages)
        self.assertIn("| Played (1): Moat", self.plr.messages)

    def test_reserve(self) -> None:
        """Test cards in reserve"""
        self.plr.messages = []
        self.plr.piles[Piles.RESERVE].set("Copper")
        Prompt.display_overview(self.plr)
        self.assertIn("| Reserve: Copper", self.plr.messages)

    def test_duration(self) -> None:
        """Test cards in duration"""
        self.plr.messages = []
        self.plr.piles[Piles.DURATION].add(self.game.get_card_from_pile("Copper"))
        Prompt.display_overview(self.plr)
        self.assertIn("| Duration: Copper", self.plr.messages)

    def test_exiled(self) -> None:
        """Test cards in exile"""
        self.plr.messages = []
        self.plr.piles[Piles.EXILE].set("Province")
        Prompt.display_overview(self.plr)
        self.assertIn("| Exile: Province", self.plr.messages)

    def test_discards(self) -> None:
        """Test cards in discards"""
        self.plr.messages = []
        self.plr.piles[Piles.DISCARD].set("Copper")
        Prompt.display_overview(self.plr)
        self.assertIn("| 1 cards in discard pile", self.plr.messages)

    def test_project(self) -> None:
        """Test having a project"""
        self.plr.messages = []
        self.plr.assign_project("Cathedral")
        Prompt.display_overview(self.plr)
        self.assertIn("| Project: Cathedral", self.plr.messages)

    def test_artifact(self) -> None:
        """Test artifact display"""
        self.plr.messages = []
        self.plr.assign_artifact("Horn")
        Prompt.display_overview(self.plr)
        self.assertIn("| Artifacts: Horn", self.plr.messages)

    def test_landmark(self) -> None:
        """Test landmark display"""
        self.plr.messages = []
        self.plr.assign_artifact("Horn")
        Prompt.display_overview(self.plr)
        for line in self.plr.messages:
            if line.startswith("| Landmark Baths"):
                break
        else:
            self.fail("Landmark message not in display")


###############################################################################
class TestBuyableSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"], badcards=["Coppersmith"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")

    def test_buy_moat(self) -> None:
        self.plr.coins.add(3)
        opts, ind = Prompt.buyable_selection(self.plr, 1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"] == "Moat":
                self.assertEqual(i["verb"], "Buy")
                self.assertEqual(i["action"], "buy")
                self.assertTrue(isinstance(i["card"], self.game.get_card_from_pile("Moat").__class__))
                break
        else:  # pragma: no coverage
            self.fail("Moat not buyable")

    def test_buy_copper(self) -> None:
        self.plr.coins.set(0)
        opts, ind = Prompt.buyable_selection(self.plr, 1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"].startswith("Copper"):
                try:
                    self.assertEqual(i["action"], "buy")
                    self.assertTrue(isinstance(i["card"], self.game.get_card_from_pile("Copper").__class__))
                except AssertionError:  # pragma: no cover
                    print(f"Buy Copper {i}")
                    self.game.print_state()
                    raise
                break
        else:  # pragma: no coverage
            self.fail("Copper not buyable")

    def test_buy_token(self) -> None:
        self.plr.coins.add(2)
        self.plr.place_token("+1 Card", "Moat")
        opts, ind = Prompt.buyable_selection(self.plr, 1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"] == "Moat":
                self.assertIn("[Tkn: +1 Card]", i["details"])
                break
        else:  # pragma: no coverage
            self.fail("Moat not buyable")


###############################################################################
class TestPlayableSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")

    def test_play(self) -> None:
        self.plr.add_card(self.moat, Piles.HAND)
        opts, ind = Prompt.playable_selection(self.plr, 1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.moat)
        self.assertEqual(opts[0]["desc"], "+2 cards, defense")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0]["name"], "Moat")
        self.assertEqual(ind, 2)

    def test_token(self) -> None:
        self.plr.place_token("+1 Card", "Moat")
        self.plr.add_card(self.moat, Piles.HAND)
        opts, ind = Prompt.playable_selection(self.plr, 1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.moat)
        self.assertIn("[Tkn: +1 Card]", opts[0]["notes"])
        self.assertEqual(ind, 2)


###############################################################################
class TestChoiceSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat", "Alchemist"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")
        self.potion = self.game.get_card_from_pile("Potion")

    def test_action_phase(self) -> None:
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.phase = Phase.ACTION
        opts = Prompt.choice_selection(self.plr)

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0]["action"], "quit")
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["verb"], "Play")
        self.assertEqual(opts[1]["name"], "Moat")
        self.assertEqual(opts[1]["action"], "play")
        self.assertEqual(opts[1]["selector"], "a")

        self.assertEqual(len(opts), 2)

    def test_buy_phase(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.phase = Phase.BUY
        self.plr.coffers = Counter("Coffer", 0)  # Stop card _choice_selection breaking test
        opts = Prompt.choice_selection(self.plr)

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0]["action"], "quit")
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["action"], "spendall")
        self.assertEqual(opts[2]["action"], "spend")

    def test_prompt(self) -> None:
        """Test prompt generation"""
        self.plr.actions.set(3)
        self.plr.buys.set(7)
        self.plr.potions.set(9)
        self.plr.coins.set(5)
        self.plr.coffers.set(1)
        self.plr.phase = Phase.BUY
        self.plr.debt = Counter("Debt", 2)
        prompt = Prompt.generate_prompt(self.plr)
        self.assertIn("Actions=3", prompt)
        self.assertIn("Coins=5", prompt)
        self.assertIn("Buys=7", prompt)
        self.assertIn("Debt=2", prompt)
        self.assertIn("Potion", prompt)
        self.assertIn("Coffer=1", prompt)

    def test_nothing_prompt(self) -> None:
        """Test that if we don't have something it doesn't appear in the prompt"""
        self.plr.actions.set(0)
        self.plr.buys.set(0)
        self.plr.potions.set(0)
        self.plr.coins.set(0)
        self.plr.coffers.set(0)
        self.plr.phase = Phase.BUY
        prompt = Prompt.generate_prompt(self.plr)
        self.assertIn("Actions=0", prompt)
        self.assertIn("Buys=0", prompt)
        self.assertNotIn("Coins", prompt)
        self.assertNotIn("Potions", prompt)
        self.assertNotIn("Coffer", prompt)


###############################################################################
class TestNightSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Monastery", "Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")

    def test_play(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Moat", "Monastery")
        opts, idx = Prompt.night_selection(self.plr, 1)
        self.assertEqual(idx, 2)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0]["action"], "play")
        self.assertEqual(opts[0]["card"].name, "Monastery")

    def test_no_night(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Moat")
        opts = Prompt.night_selection(self.plr, 0)
        self.assertEqual(opts, ([], 0))


###############################################################################
class TestSpendableSelection(unittest.TestCase):
    """Test _spendable_selection()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(
            numplayers=1,
            initcards=["Moat", "Alchemist"],
            badcards=["Baker"],
        )
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")
        self.potion = self.game.get_card_from_pile("Potion")

    def test_play(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.add_card(self.potion, Piles.HAND)
        self.plr.add_card(self.moat, Piles.HAND)
        self.plr.coffers.add(1)
        self.plr.villagers.add(1)
        opts = Prompt.spendable_selection(self.plr)
        self.assertEqual(opts[0]["selector"], "1")
        self.assertEqual(opts[0]["action"], "spendall")
        self.assertIn("Spend all treasures", opts[0]["verb"])
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["selector"], "2")
        self.assertEqual(opts[1]["verb"], "Spend Coffer (1 coin)")
        self.assertEqual(opts[1]["action"], "coffer")
        self.assertIsNone(opts[1]["card"])

        self.assertEqual(opts[2]["selector"], "4")
        self.assertEqual(opts[2]["verb"], "Spend")
        self.assertEqual(opts[2]["name"], "Copper")
        self.assertEqual(opts[2]["action"], "spend")
        self.assertEqual(opts[2]["card"].name, "Copper")

        self.assertEqual(opts[3]["verb"], "Spend")
        self.assertEqual(opts[3]["selector"], "5")
        self.assertEqual(opts[3]["action"], "spend")
        self.assertEqual(opts[3]["card"].name, "Potion")

    def test_debt(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.debt = Counter("Debt", 1)
        self.plr.coins.set(1)
        self.plr.coffers = Counter("Coffer", 0)
        try:
            opts = Prompt.spendable_selection(self.plr)
            self.assertEqual(opts[1]["selector"], "3")
            self.assertEqual(opts[1]["action"], "payback")
            self.assertEqual(opts[1]["verb"], "Payback Debt")
            self.assertIsNone(opts[1]["card"])
        except AssertionError:  # pragma: no cover
            self.game.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
