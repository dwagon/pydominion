#!/usr/bin/env python
# pylint: disable=protected-access
"""Testing prompt code"""

import unittest

from dominion import Game, Phase, Piles, Prompt, Token, Action
from dominion.Counter import Counter


###############################################################################
class TestDisplayOverview(unittest.TestCase):
    """Test the display overview at the start of every user input"""

    def setUp(self) -> None:
        self.game = Game.TestGame(
            numplayers=1,
            initcards=["Moat", "Border Guard"],
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
        else:  # pragma: no coverage
            self.fail("Landmark message not in display")


###############################################################################
class TestCanBuy(unittest.TestCase):
    """Test can_buy()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")

    def test_debt(self) -> None:
        self.assertTrue(Prompt.can_buy(self.plr, self.moat, [self.moat]))
        self.plr.debt.set(1)
        self.assertFalse(Prompt.can_buy(self.plr, self.moat, [self.moat]))

    def test_buys(self) -> None:
        self.plr.buys.set(1)
        self.assertTrue(Prompt.can_buy(self.plr, self.moat, [self.moat]))
        self.plr.buys.set(0)
        self.assertFalse(Prompt.can_buy(self.plr, self.moat, [self.moat]))

    def test_not_affordable(self) -> None:
        self.assertTrue(Prompt.can_buy(self.plr, self.moat, [self.moat]))
        self.assertFalse(Prompt.can_buy(self.plr, self.moat, []))


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
                self.assertEqual(i["action"], Action.BUY)
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
                    self.assertEqual(i["action"], Action.BUY)
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
        self.plr.place_token(Token.PLUS_1_CARD, "Moat")
        opts, ind = Prompt.buyable_selection(self.plr, 1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"] == "Moat":
                self.assertIn("[Tkn: +1 Card]", i["details"])
                break
        else:  # pragma: no coverage
            self.fail("Moat not buyable")


###############################################################################
class TestWaySelection(unittest.TestCase):
    """Test way_selection()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat", "Way of the Camel"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")

    def test_selection(self) -> None:
        opts, ind = Prompt.way_selection(self.plr, self.moat, 1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")  # "a" is for Moat
        self.assertEqual(opts[0]["name"], "Way of the Camel")
        self.assertEqual(opts[0]["desc"], "Moat: Exile a Gold from the Supply.")
        self.assertEqual(opts[0]["action"], Action.WAY)

    def test_no_ways(self) -> None:
        """No way should return emptiness"""
        game = Game.TestGame(numplayers=1, initcards=["Moat"])
        game.start_game()
        plr = game.player_list()[0]
        moat = game.get_card_from_pile("Moat")
        opts, ind = Prompt.way_selection(plr, moat, 1)

        self.assertEqual(len(opts), 0)
        self.assertEqual(ind, 1)


###############################################################################
class TestPlayableSelection(unittest.TestCase):
    """Test playable_selection()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat", "Alley"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")
        self.alley = self.game.get_card_from_pile("Alley")

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
        self.plr.place_token(Token.PLUS_1_CARD, "Moat")
        self.plr.add_card(self.moat, Piles.HAND)
        opts, ind = Prompt.playable_selection(self.plr, 1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.moat)
        self.assertIn("[Tkn: +1 Card]", opts[0]["notes"])
        self.assertEqual(ind, 2)

    def test_villager(self) -> None:
        """Test using a villager"""
        self.plr.villagers.set(1)
        opts, ind = Prompt.playable_selection(self.plr, 1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "1")
        self.assertIsNone(opts[0]["card"])
        self.assertEqual(opts[0]["action"], Action.VILLAGER)
        self.assertEqual(ind, 1)

    def test_shadow(self) -> None:
        """Shadows should be playable from deck"""
        self.plr.add_card(self.alley, Piles.DECK)
        opts, ind = Prompt.playable_selection(self.plr, 1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.alley)
        self.assertEqual(opts[0]["desc"], "+1 Card. +1 Action. Discard a card.")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0]["name"], "Alley")
        self.assertEqual(ind, 2)


###############################################################################
class TestChoiceSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat", "Alchemist", "Guardian"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")
        self.potion = self.game.get_card_from_pile("Potion")

    def test_action_phase(self) -> None:
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.phase = Phase.ACTION
        opts = Prompt.choice_selection(self.plr)

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0]["action"], Action.QUIT)
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["verb"], "Play")
        self.assertEqual(opts[1]["name"], "Moat")
        self.assertEqual(opts[1]["action"], Action.PLAY)
        self.assertEqual(opts[1]["selector"], "a")

        self.assertEqual(len(opts), 2)

    def test_buy_phase(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.phase = Phase.BUY
        self.plr.coffers = Counter("Coffer", 0)  # Stop card choice_selection breaking test
        opts = Prompt.choice_selection(self.plr)

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0]["action"], Action.QUIT)
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["action"], Action.SPENDALL)
        self.assertEqual(opts[2]["action"], Action.SPEND)

    def test_night_phase(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Guardian")
        self.plr.phase = Phase.NIGHT
        self.plr.coffers = Counter("Coffer", 0)  #
        opts = Prompt.choice_selection(self.plr)

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0]["action"], Action.QUIT)
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["action"], Action.PLAY)
        self.assertEqual(opts[1]["name"], "Guardian")
        self.assertEqual(opts[1]["selector"], "a")

    def test_prompt(self) -> None:
        """Test prompt generation"""
        self.plr.actions.set(3)
        self.plr.buys.set(7)
        self.plr.potions.set(9)
        self.plr.coins.set(5)
        self.plr.coffers.set(1)
        self.plr.villagers.set(3)
        self.plr.phase = Phase.BUY
        self.plr.debt = Counter("Debt", 2)
        prompt = Prompt.generate_prompt(self.plr)
        self.assertIn("Actions=3", prompt)
        self.assertIn("Coins=5", prompt)
        self.assertIn("Buys=7", prompt)
        self.assertIn("Debt=2", prompt)
        self.assertIn("Potion", prompt)
        self.assertIn("Coffer=1", prompt)
        self.assertIn("Villager=3", prompt)

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
        self.assertEqual(opts[0]["action"], Action.PLAY)
        self.assertEqual(opts[0]["card"].name, "Monastery")

    def test_no_night(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Moat")
        opts = Prompt.night_selection(self.plr, 0)
        self.assertEqual(opts, ([], 0))


###############################################################################
class TestProjectSelection(unittest.TestCase):
    """Test project_selection()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(
            numplayers=1,
            project_path="tests/projects",
            projects=["ProjectA"],
        )
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_projects_no_buy(self) -> None:
        opts, idx = Prompt.project_selection(self.plr, 0)
        self.assertEqual(idx, 1)
        self.assertEqual(opts[0]["selector"], "-")
        self.assertEqual(opts[0]["action"], Action.NONE)
        self.assertEqual(opts[0]["card"].name, "ProjectA")

    def test_projects_buy(self) -> None:
        self.plr.coins.add(5)
        opts, idx = Prompt.project_selection(self.plr, 0)
        self.assertEqual(idx, 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["action"], Action.PROJECT)
        self.assertEqual(opts[0]["card"].name, "ProjectA")


###############################################################################
class TestSpendAllDetails(unittest.TestCase):
    """Test spend_all_details()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(
            numplayers=1,
            initcards=["Moat", "Alchemist"],
        )
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_total(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        spendable = [_ for _ in self.plr.piles[Piles.HAND] if _.isTreasure()]
        self.assertEqual(Prompt.spend_all_details(self.plr, spendable), "6 coin")

    def test_potion(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Potion")
        spendable = [_ for _ in self.plr.piles[Piles.HAND] if _.isTreasure()]
        self.assertEqual(Prompt.spend_all_details(self.plr, spendable), "3 coin, 1 potions")


###############################################################################
class TestDisplayTokens(unittest.TestCase):
    """Test display_tokens()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_display_journey(self) -> None:
        self.assertEqual(Prompt.display_tokens(self.plr), "Journey Faceup")
        self.plr.flip_journey_token()
        self.assertEqual(Prompt.display_tokens(self.plr), "Journey Facedown")

    def test_plus_card_token(self) -> None:
        self.assertNotIn("+1 Card: Moat", Prompt.display_tokens(self.plr))
        self.plr.place_token(Token.PLUS_1_CARD, "Moat")
        self.assertIn("+1 Card: Moat", Prompt.display_tokens(self.plr))

    def test_plus_one_action(self) -> None:
        self.assertNotIn("+1 Action: Moat", Prompt.display_tokens(self.plr))
        self.plr.place_token(Token.PLUS_1_ACTION, "Moat")
        self.assertIn("+1 Action: Moat", Prompt.display_tokens(self.plr))

    def test_plus_one_buy(self) -> None:
        self.assertNotIn("+1 Buy: Moat", Prompt.display_tokens(self.plr))
        self.plr.place_token(Token.PLUS_1_BUY, "Moat")
        self.assertIn("+1 Buy: Moat", Prompt.display_tokens(self.plr))

    def test_plus_one_coin(self) -> None:
        self.assertNotIn("+1 Coin: Moat", Prompt.display_tokens(self.plr))
        self.plr.place_token(Token.PLUS_1_COIN, "Moat")
        self.assertIn("+1 Coin: Moat", Prompt.display_tokens(self.plr))

    def test_minus_one_card(self) -> None:
        self.assertNotIn("-1 Card: Moat", Prompt.display_tokens(self.plr))
        self.plr.place_token(Token.MINUS_1_CARD, "Moat")
        self.assertIn("-1 Card: Moat", Prompt.display_tokens(self.plr))

    def test_minus_one_coin(self) -> None:
        self.assertNotIn("-1 Coin: Moat", Prompt.display_tokens(self.plr))
        self.plr.place_token(Token.MINUS_1_COIN, "Moat")
        self.assertIn("-1 Coin: Moat", Prompt.display_tokens(self.plr))


###############################################################################
class TestSpendableSelection(unittest.TestCase):
    """Test spendable_selection()"""

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
        self.assertEqual(opts[0]["action"], Action.SPENDALL)
        self.assertIn("Spend all treasures", opts[0]["verb"])
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["selector"], "2")
        self.assertEqual(opts[1]["verb"], "Spend Coffer (+1 coin)")
        self.assertEqual(opts[1]["action"], Action.COFFER)
        self.assertIsNone(opts[1]["card"])

        self.assertEqual(opts[2]["selector"], "4")
        self.assertEqual(opts[2]["verb"], "Spend")
        self.assertEqual(opts[2]["name"], "Copper")
        self.assertEqual(opts[2]["action"], Action.SPEND)
        self.assertEqual(opts[2]["card"].name, "Copper")

        self.assertEqual(opts[3]["verb"], "Spend")
        self.assertEqual(opts[3]["selector"], "5")
        self.assertEqual(opts[3]["action"], Action.SPEND)
        self.assertEqual(opts[3]["card"].name, "Potion")

    def test_debt(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.debt = Counter("Debt", 1)
        self.plr.coins.set(1)
        self.plr.coffers = Counter("Coffer", 0)
        try:
            opts = Prompt.spendable_selection(self.plr)
            self.assertEqual(opts[1]["selector"], "3")
            self.assertEqual(opts[1]["action"], Action.PAYBACK)
            self.assertEqual(opts[1]["verb"], "Payback Debt")
            self.assertIsNone(opts[1]["card"])
        except AssertionError:  # pragma: no cover
            self.game.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
