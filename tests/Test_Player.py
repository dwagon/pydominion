#!/usr/bin/env python
# pylint: disable=protected-access
""" Testing player code """

import unittest
from dominion.Counter import Counter
from dominion import Card, Game
from dominion.Player import Phase


###############################################################################
class TestPlayer(unittest.TestCase):
    """Test cases for Player class"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_initialCardStacks(self):
        """Make sure initial hands are correct"""
        self.assertEqual(len(self.plr.deck), 5)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.played.size(), 0)
        self.assertEqual(self.plr.discardpile.size(), 0)

    def test_initialDeck(self):
        """Ensure initial player decks are correct"""
        self.plr.deck.empty()
        self.plr._initial_deck(heirlooms=[])
        self.assertEqual(len(self.plr.deck), 10)

    def test_trashcard_hand(self):
        """Test that trashing a card from hand works"""
        num_cards = self.game.count_cards()
        card = self.plr.hand[0]
        self.plr.trash_card(card)
        self.assertEqual(num_cards, self.game.count_cards())
        self.assertIn(card, self.game.trashpile)

    def test_trashcard_played(self):
        """Test that trashing a card from played works"""
        self.plr.played.set("Estate")
        num_cards = self.game.count_cards()
        card = self.plr.played[0]
        self.plr.trash_card(card)
        self.assertIn(card, self.game.trashpile)
        self.assertEqual(num_cards, self.game.count_cards())

    def test_deckorder(self):
        """Ensure adding cards to decks in the correct order"""
        self.plr.deck.empty()
        estate = self.game["Estate"].remove()
        gold = self.game["Gold"].remove()
        self.plr.add_card(estate, "deck")
        self.plr.add_card(gold, "topdeck")
        crd = self.plr.next_card()
        self.assertEqual(crd.name, "Gold")


###############################################################################
class test_discard_hand(unittest.TestCase):
    """Test plr.discard_hand()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_discard(self):
        """Test discard_hand()"""
        self.plr.hand.set("Copper", "Silver")
        self.plr.played.set("Estate", "Duchy")
        self.plr.discard_hand()
        self.assertEqual(self.plr.hand.size(), 0)
        self.assertEqual(self.plr.played.size(), 0)
        self.assertEqual(self.plr.discardpile.size(), 4)


###############################################################################
class Test_next_card(unittest.TestCase):
    """Test next_card()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_emptyDeck(self):
        """test empty deck"""
        self.plr.deck.empty()
        self.plr.discardpile.set("Gold")
        c = self.plr.next_card()
        self.assertEqual(c.name, "Gold")

    def test_noCards(self):
        """Test that an empty deck has no cards"""
        self.plr.deck.empty()
        self.plr.discardpile.empty()
        c = self.plr.next_card()
        self.assertIsNone(c)

    def test_drawOne(self):
        self.plr.deck.set("Province")
        self.plr.discardpile.empty()
        c = self.plr.next_card()
        self.assertEqual(c.name, "Province")
        self.assertTrue(self.plr.deck.is_empty())


###############################################################################
class Test_playonce(unittest.TestCase):
    """Test the play once capability"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_once(self):
        x = self.plr.do_once("test")
        self.assertTrue(x)
        x = self.plr.do_once("test")
        self.assertFalse(x)


###############################################################################
class Test_cards_affordable(unittest.TestCase):
    """Test the cards_affordable functionality"""

    def setUp(self):
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
            ],
        )
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_under(self):
        """Test cards under a cost"""
        price = 4
        ans = self.plr.cards_under(price, types={Card.CardType.ACTION: True})
        for a in ans:
            try:
                self.assertLessEqual(a.cost, price)
                self.assertTrue(a.isAction())
            except AssertionError:  # pragma: no cover
                print(f"{a=}")
                self.game.print_state()
                raise

    def test_worth(self):
        """Test cards equal to a cost"""
        price = 5
        ans = self.plr.cards_worth(price, types={Card.CardType.VICTORY: True})
        for a in ans:
            self.assertEqual(a.cost, price)
            self.assertTrue(a.isVictory())

    def test_nocost(self):
        """Test with no cost"""
        ans = self.plr.cards_affordable(
            "less",
            coin=None,
            num_potions=0,
            types={
                Card.CardType.VICTORY: True,
                Card.CardType.ACTION: True,
                Card.CardType.TREASURE: True,
                Card.CardType.NIGHT: True,
            },
        )
        self.assertIn("Province", [cp.name for cp in ans])


###############################################################################
class Test__type_selector(unittest.TestCase):
    """Test _type_selector()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_selzero(self):
        """Test selecting zero types"""
        x = self.plr._type_selector({})
        self.assertTrue(x[Card.CardType.ACTION])
        self.assertTrue(x[Card.CardType.TREASURE])
        self.assertTrue(x[Card.CardType.VICTORY])

    def test_selone(self):
        """Test selecting one type"""
        x = self.plr._type_selector({Card.CardType.ACTION: True})
        self.assertTrue(x[Card.CardType.ACTION])
        self.assertFalse(x[Card.CardType.TREASURE])
        self.assertFalse(x[Card.CardType.VICTORY])

    def test_seltwo(self):
        """Test selecting two types"""
        x = self.plr._type_selector({Card.CardType.ACTION: True, Card.CardType.VICTORY: True})
        self.assertTrue(x[Card.CardType.ACTION])
        self.assertFalse(x[Card.CardType.TREASURE])
        self.assertTrue(x[Card.CardType.VICTORY])


###############################################################################
class Test_plr_trash_card(unittest.TestCase):
    """Test plr_trash_card()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_None(self):
        """Trash nothing"""
        self.plr.hand.set("Gold")
        self.plr.test_input = ["0"]
        x = self.plr.plr_trash_card()
        self.assertEqual(x, [])
        self.assertNotIn("Gold", self.game.trashpile)

    def test_Two(self):
        """Trash Two cards"""
        self.plr.hand.set("Gold", "Copper", "Silver")
        self.plr.test_input = ["Gold", "Silver", "0"]
        x = self.plr.plr_trash_card(num=2)
        self.assertEqual(len(x), 2)
        self.assertIn("Gold", self.game.trashpile)
        self.assertIn("Silver", self.game.trashpile)
        self.assertIn("Copper", self.plr.hand)

    def test_Trash(self):
        """Test trashing"""
        tsize = self.game.trashpile.size()
        self.plr.hand.set("Gold")
        self.plr.test_input = ["1"]
        x = self.plr.plr_trash_card()
        self.assertEqual(x[0].name, "Gold")
        self.assertEqual(self.game.trashpile.size(), tsize + 1)
        self.assertIn("Gold", self.game.trashpile)

    def test_force(self):
        """Test trashing a card with force"""
        self.game.trashpile.set()
        self.plr.hand.set("Gold")
        self.plr.test_input = ["0", "1"]
        x = self.plr.plr_trash_card(force=True)
        self.assertEqual(x[0].name, "Gold")
        self.assertEqual(self.game.trashpile[-1].name, "Gold")
        for m in self.plr.messages:
            if "Invalid Option" in m:
                break
        else:  # pragma: no cover
            self.fail("Accepted none when force")
        for m in self.plr.messages:
            if "Trash nothing" in m:  # pragma: no cover
                self.fail("Nothing available")

    def test_exclude(self):
        """Test that the 'exclude' option works by not being able to select"""
        self.plr.hand.set("Gold", "Gold", "Copper")
        self.plr.test_input = ["1"]
        x = self.plr.plr_trash_card(exclude=["Gold"])
        self.assertEqual(x[0].name, "Copper")
        self.assertIn("Copper", self.game.trashpile)


###############################################################################
class Test_plrDiscardCard(unittest.TestCase):
    """Test the plr_discard_cards() function"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_discardNone(self):
        self.plr.hand.set("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["0"]
        x = self.plr.plr_discard_cards(0)
        self.assertEqual(x, [])
        self.assertEqual(len(self.plr.hand), 4)
        self.assertTrue(self.plr.discardpile.is_empty())

    def test_discardOne(self):
        self.plr.hand.set("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["1", "0"]
        x = self.plr.plr_discard_cards(1)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile._cards)

    def test_discardAnynum(self):
        self.plr.hand.set("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["1", "0"]
        x = self.plr.plr_discard_cards(0, anynum=True)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile)


###############################################################################
class Test_attack_victims(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=3, initcards=["Moat"])
        self.game.start_game()
        self.plr, self.defend, self.victim = self.game.player_list()
        self.defend.hand.set("Moat")

    def test_output(self):
        v = self.plr.attack_victims()
        self.assertEqual(v, [self.victim])


###############################################################################
class Test_gain_card(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_gainByString(self):
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.discardpile[0].name, "Copper")

    def test_gainByCardpile(self):
        cp = self.game["Copper"]
        self.plr.gain_card(cp)
        self.assertEqual(self.plr.discardpile[0].name, "Copper")

    def test_gainSpecific(self):
        cu = self.game["Copper"].remove()
        self.plr.gain_card(newcard=cu)
        self.assertEqual(self.plr.discardpile[0].name, "Copper")

    def test_destination(self):
        self.plr.hand.empty()
        self.plr.gain_card("Copper", "hand")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand[0].name, "Copper")


###############################################################################
class Test__spend_all_cards(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_spendCards(self):
        """Spend all cards in hand"""
        self.plr.hand.set("Gold", "Silver", "Estate", "Moat")
        self.plr._spend_all_cards()
        self.assertEqual(self.plr.coins.get(), 3 + 2)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(len(self.plr.played), 2)
        for c in self.plr.played:
            if not c.isTreasure():  # pragma: no cover
                self.fail("Spent non treasure")


###############################################################################
class Test_pickup_card(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_pickup(self):
        """Test picking up a card"""
        self.plr.deck.set("Gold")
        self.plr.hand.set()
        self.plr.pickup_card()
        self.assertEqual(self.plr.hand[0].name, "Gold")
        self.assertEqual(self.plr.deck.size(), 0)
        self.assertEqual(self.plr.hand.size(), 1)

    def test_pickup_empty(self):
        """Test picking up a card from an empty deck"""
        self.plr.deck.set()
        self.plr.discardpile.set("Gold")
        self.plr.hand.set()
        self.plr.pickup_card()
        self.assertEqual(self.plr.hand[0].name, "Gold")
        self.assertEqual(self.plr.deck.size(), 0)
        self.assertEqual(self.plr.hand.size(), 1)

    def test_pick_nomore(self):
        """Test picking up a card when there isn't one to be had"""
        self.plr.deck.set()
        self.plr.discardpile.set()
        self.plr.hand.set()
        c = self.plr.pickup_card()
        self.assertIsNone(c)
        self.assertEqual(self.plr.hand.size(), 0)

    def test_pickups(self):
        """Test pickup_cards"""
        self.plr.hand.set()
        self.plr.pickup_cards(3, verb="test")
        self.assertEqual(self.plr.hand.size(), 3)
        count = 0
        for msg in self.plr.messages:
            if "test" in msg:
                count += 1
        self.assertEqual(count, 3)


###############################################################################
class Test_misc(unittest.TestCase):
    """Test misc functions"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Golem", "Witch", "Engineer"])
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_coststr(self):
        """Test coststr()"""
        witch = self.game["Witch"].remove()
        golem = self.game["Golem"].remove()
        eng = self.game["Engineer"].remove()
        self.assertEqual(self.plr.coststr(witch), "3 Coins")
        self.assertEqual(self.plr.coststr(golem), "4 Coins, Potion")
        self.assertEqual(self.plr.coststr(eng), "0 Coins, 4 Debt")

    def test_durationpile_size(self):
        copper = self.game["Copper"].remove()
        self.assertEqual(self.plr.durationpile.size(), 0)
        self.plr.durationpile.add(copper)
        self.plr.durationpile.add(copper)
        self.assertEqual(self.plr.durationpile.size(), 2)

    def test_cleanup_phase(self):
        self.plr.hand.set("Copper")
        self.plr.cleanup_phase()
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.played.size(), 0)


###############################################################################
class Test_score(unittest.TestCase):
    """Test score related functions"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_add_score(self):
        """Test add_score()"""
        self.plr.add_score("Bunny", 3)
        self.assertEqual(self.plr.score["Bunny"], 3)

    def test_get_score(self):
        """Test get_score()"""
        pre = self.plr.get_score()
        self.plr.discardpile.set("Province")
        self.assertEqual(self.plr.get_score(), pre + 6)

    def test_get_score_details(self):
        """Test get_score_details()"""
        self.assertEqual(self.plr.get_score_details()["Estate"], 3)
        self.plr.add_score("Bunny", 5)
        self.assertEqual(self.plr.get_score_details()["Bunny"], 5)


###############################################################################
class Test_start_turn(unittest.TestCase):
    """Test the start_turn()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_start_turn_changes(self):
        """Make sure lots of changes are reset"""
        self.plr.phase = Phase.NONE
        self.plr.coins.set(5)
        self.plr.start_turn()
        self.assertEqual(self.plr.phase, Phase.START)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.stats["gained"], [])
        self.assertEqual(self.plr.stats["bought"], [])


###############################################################################
class Test_defer(unittest.TestCase):
    """Test deferring cards"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_defer_card(self):
        """Test defer_card()"""
        moat = self.game["Moat"].remove()
        self.plr.defer_card(moat)
        self.assertIn("Moat", self.plr.deferpile)

    def test_defer_start_turn(self):
        """Make sure we run the deferpile"""
        moat = self.game["Moat"].remove()
        self.plr.defer_card(moat)
        self.assertEqual(self.plr.actions.get(), 1)
        self.plr._defer_start_turn()
        self.assertIn("Moat", self.plr.played)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
class Test__display_overview(unittest.TestCase):
    """Test the display overview at the start of every user input"""

    def setUp(self):
        self.game = Game.TestGame(
            numplayers=1, initcards=["Moat"], initprojects=["Cathedral"], landmarkcards=["Baths"]
        )
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_empty(self):
        """When we have empty hands"""
        self.plr.messages = []
        self.plr.hand.set()
        self.plr.played.set()
        self.plr._display_overview()
        self.assertIn("| Hand: <EMPTY>", self.plr.messages)
        self.assertIn("| Played: <NONE>", self.plr.messages)

    def test_non_empty(self):
        """Test not empty hand"""
        self.plr.messages = []
        self.plr.hand.set("Copper", "Estate")
        self.plr.played.set("Moat")
        self.plr._display_overview()
        self.assertIn("| Hand: Copper, Estate", self.plr.messages)
        self.assertIn("| Played: Moat", self.plr.messages)

    def test_reserve(self):
        """Test cards in reserve"""
        self.plr.messages = []
        self.plr.reserve.set("Copper")
        self.plr._display_overview()
        self.assertIn("| Reserve: Copper", self.plr.messages)

    def test_duration(self):
        """Test cards in duration"""
        self.plr.messages = []
        self.plr.durationpile.add(self.game["Copper"].remove())
        self.plr._display_overview()
        self.assertIn("| Duration: Copper", self.plr.messages)

    def test_exiled(self):
        """Test cards in exile"""
        self.plr.messages = []
        self.plr.exilepile.set("Province")
        self.plr._display_overview()
        self.assertIn("| Exile: Province", self.plr.messages)

    def test_discards(self):
        """Test cards in discards"""
        self.plr.messages = []
        self.plr.discardpile.set("Copper")
        self.plr._display_overview()
        self.assertIn("| 1 cards in discard pile", self.plr.messages)

    def test_project(self):
        """Test having a project"""
        self.plr.messages = []
        self.plr.assign_project("Cathedral")
        self.plr._display_overview()
        self.assertIn("| Project: Cathedral", self.plr.messages)

    def test_artifact(self):
        """Test artifact display"""
        self.plr.messages = []
        self.plr.assign_artifact("Horn")
        self.plr._display_overview()
        self.assertIn("| Artifacts: Horn", self.plr.messages)

    def test_landmark(self):
        """Test landmark display"""
        self.plr.messages = []
        self.plr.assign_artifact("Horn")
        self.plr._display_overview()
        for line in self.plr.messages:
            if line.startswith("| Landmark Baths"):
                break
        else:
            self.fail("Landmark message not in display")


###############################################################################
class Test__buyable_selection(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"], badcards=["Coppersmith"])
        self.game.start_game()
        self.plr = self.game.player_list(0)
        self.moat = self.game["Moat"].remove()

    def test_buy_moat(self):
        self.plr.coins.add(3)
        opts, ind = self.plr._buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"] == "Moat":
                self.assertEqual(i["verb"], "Buy")
                self.assertEqual(i["action"], "buy")
                self.assertEqual(i["card"], self.game["Moat"])
                break
        else:  # pragma: no coverage
            self.fail("Moat not buyable")

    def test_buy_copper(self):
        self.plr.coins.set(0)
        opts, ind = self.plr._buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"].startswith("Copper"):
                try:
                    self.assertEqual(i["action"], "buy")
                    self.assertEqual(i["card"], self.game["Copper"])
                except AssertionError:  # pragma: no cover
                    print(f"Buy Copper {i}")
                    self.game.print_state()
                    raise
                break
        else:  # pragma: no coverage
            self.fail("Copper not buyable")

    def test_buy_token(self):
        self.plr.coins.add(2)
        self.plr.place_token("+1 Card", "Moat")
        opts, ind = self.plr._buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"] == "Moat":
                self.assertIn("[Tkn: +1 Card]", i["details"])
                break
        else:  # pragma: no coverage
            self.fail("Moat not buyable")


###############################################################################
class Test__playable_selection(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list(0)
        self.moat = self.game["Moat"].remove()

    def test_play(self):
        self.plr.add_card(self.moat, "hand")
        opts, ind = self.plr._playable_selection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.moat)
        self.assertEqual(opts[0]["desc"], "+2 cards, defense")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0]["name"], "Moat")
        self.assertEqual(ind, 2)

    def test_token(self):
        self.plr.place_token("+1 Card", "Moat")
        self.plr.add_card(self.moat, "hand")
        opts, ind = self.plr._playable_selection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.moat)
        self.assertTrue("[Tkn: +1 Card]" in opts[0]["notes"])
        self.assertEqual(ind, 2)


###############################################################################
class Test__choice_selection(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Moat", "Alchemist"])
        self.game.start_game()
        self.plr = self.game.player_list(0)
        self.moat = self.game["Moat"].remove()
        self.potion = self.game["Potion"].remove()

    def test_action_phase(self):
        self.plr.hand.set("Moat")
        self.plr.phase = Phase.ACTION
        opts, _ = self.plr._choice_selection()

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0]["action"], "quit")
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["verb"], "Play")
        self.assertEqual(opts[1]["name"], "Moat")
        self.assertEqual(opts[1]["action"], "play")
        self.assertEqual(opts[1]["selector"], "a")

        self.assertEqual(len(opts), 2)

    def test_buy_phase(self):
        self.plr.hand.set("Copper")
        self.plr.phase = Phase.BUY
        self.plr.coffers = Counter("Coffer", 0)  # Stop card _choice_selection breaking test
        opts, _ = self.plr._choice_selection()

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0]["action"], "quit")
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["action"], "spendall")
        self.assertEqual(opts[2]["action"], "spend")

    def test_prompt(self):
        """Test prompt generation"""
        self.plr.actions.set(3)
        self.plr.buys.set(7)
        self.plr.potions.set(9)
        self.plr.coins.set(5)
        self.plr.coffers.set(1)
        self.plr.phase = "buy"
        self.plr.debt = Counter("Debt", 2)
        _, prompt = self.plr._choice_selection()
        self.assertIn("Actions=3", prompt)
        self.assertIn("Coins=5", prompt)
        self.assertIn("Buys=7", prompt)
        self.assertIn("Debt=2", prompt)
        self.assertIn("Potion", prompt)
        self.assertIn("Coffer=1", prompt)

    def test_nothing_prompt(self):
        """Test that if we don't have something it doesn't appear in the prompt"""
        self.plr.actions.set(0)
        self.plr.buys.set(0)
        self.plr.potions.set(0)
        self.plr.coins.set(0)
        self.plr.coffers.set(0)
        self.plr.phase = "buy"
        _, prompt = self.plr._choice_selection()
        self.assertIn("Actions=0", prompt)
        self.assertIn("Buys=0", prompt)
        self.assertNotIn("Coins", prompt)
        self.assertNotIn("Potions", prompt)
        self.assertNotIn("Coffer", prompt)


###############################################################################
class Test__night_selection(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1, initcards=["Monastery", "Moat"])
        self.game.start_game()
        self.plr = self.game.player_list(0)
        self.moat = self.game["Moat"].remove()

    def test_play(self):
        self.plr.hand.set("Copper", "Moat", "Monastery")
        opts, idx = self.plr._night_selection(1)
        self.assertEqual(idx, 2)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0]["action"], "play")
        self.assertEqual(opts[0]["card"].name, "Monastery")

    def test_no_night(self):
        self.plr.hand.set("Copper", "Moat")
        opts = self.plr._night_selection(0)
        self.assertEqual(opts, ([], 0))


###############################################################################
class Test__spendable_selection(unittest.TestCase):
    """Test _spendable_selection()"""

    def setUp(self):
        self.game = Game.TestGame(
            numplayers=1,
            initcards=["Moat", "Alchemist"],
            badcards=["Baker"],
        )
        self.game.start_game()
        self.plr = self.game.player_list(0)
        self.moat = self.game["Moat"].remove()
        self.potion = self.game["Potion"].remove()

    def test_play(self):
        self.plr.hand.set("Copper", "Estate")
        self.plr.add_card(self.potion, "hand")
        self.plr.add_card(self.moat, "hand")
        self.plr.coffers.add(1)
        self.plr.villagers.add(1)
        opts = self.plr._spendable_selection()
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

    def test_debt(self):
        self.plr.hand.set("Copper")
        self.plr.debt = Counter("Debt", 1)
        self.plr.coins.set(1)
        self.plr.coffers = Counter("Coffer", 0)
        try:
            opts = self.plr._spendable_selection()
            self.assertEqual(opts[1]["selector"], "3")
            self.assertEqual(opts[1]["action"], "payback")
            self.assertEqual(opts[1]["verb"], "Payback Debt")
            self.assertIsNone(opts[1]["card"])
        except AssertionError:  # pragma: no cover
            self.game.print_state()
            raise


###############################################################################
class Test_buy_card(unittest.TestCase):
    """Test buy_card()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1, oldcards=True, initcards=["Embargo"])
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_debt(self):
        """Test buying a card when the player has a debt"""
        self.plr.debt = Counter("Debt", 1)
        self.plr.buy_card(self.game["Copper"])
        self.assertIn("Must pay off debt first", self.plr.messages)

    def test_embargo(self):
        """Test buying an embargoed card"""
        self.game["Copper"].embargo()
        self.plr.buy_card(self.game["Copper"])
        self.assertIsNotNone(self.plr.discardpile["Curse"])
        self.assertIn("Gained a Curse from embargo", self.plr.messages)


###############################################################################
class Test_spend_coffer(unittest.TestCase):
    """Test spending coffers"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_spend_coffer(self):
        """Spend a coffer that the player has"""
        self.plr.coffers = Counter("Coffer", 1)
        self.plr.spend_coffer()
        self.assertEqual(self.plr.coffers.get(), 0)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_spendNothing(self):
        """Spend a coffer that the player doesn't have"""
        self.plr.coffers = Counter("Coffer", 0)
        self.plr.spend_coffer()
        self.assertEqual(self.plr.coffers.get(), 0)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
class Test_spend_villager(unittest.TestCase):
    """Test spend_villager()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_spend_villager(self):
        """Spend a Villager that the player has"""
        self.plr.villagers.set(1)
        self.plr.spend_villager()
        self.assertEqual(self.plr.villagers.get(), 0)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_spendNothing(self):
        """Spend a Villager that the player doesn't have"""
        self.plr.villagers.set(0)
        self.plr.spend_villager()
        self.assertEqual(self.plr.villagers.get(), 0)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
class Test_plr_gain_card(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_gain_card_equal(self):
        self.plr.test_input = ["get silver"]
        c = self.plr.plr_gain_card(3, modifier="equal")
        self.assertIsNotNone(self.plr.discardpile["Silver"])
        self.assertEqual(c.name, "Silver")

    def test_gain_card_less(self):
        self.plr.test_input = ["get silver"]
        c = self.plr.plr_gain_card(4, modifier="less")
        self.assertIsNotNone(self.plr.discardpile["Silver"])
        self.assertEqual(c.name, "Silver")


###############################################################################
class Test_exile(unittest.TestCase):
    """Test exile pile"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_exile_card(self):
        """Test exiling a card"""
        au_card = self.game["Gold"].remove()
        self.plr.exilepile.empty()
        self.plr.exile_card(au_card)
        self.assertIn("Gold", self.plr.exilepile)

    def test_unexiling_card(self):
        """Test un-exiling a card"""
        self.plr.exilepile.set("Gold", "Gold", "Silver")
        self.plr.test_input = ["Unexile"]
        self.plr.gain_card("Gold")
        self.assertEqual(len(self.plr.discardpile), 3)
        self.assertEqual(len(self.plr.exilepile), 1)
        self.assertNotIn("Gold", self.plr.exilepile)
        self.assertIn("Silver", self.plr.exilepile)


###############################################################################
class Test_plr_discard_down_to(unittest.TestCase):
    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_discard_nothing(self):
        self.plr.hand.set("Estate", "Duchy", "Province")
        self.plr.plr_discard_down_to(3)
        self.assertEqual(self.plr.discardpile.size(), 0)

    def test_discard_one(self):
        self.plr.test_input = ["gold", "finish"]
        self.plr.hand.set("Estate", "Duchy", "Province", "Gold")
        self.plr.plr_discard_down_to(3)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertIsNotNone(self.plr.discardpile["Gold"])


###############################################################################
class Test_Add_Card(unittest.TestCase):
    """Test add_card()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_add(self):
        """Add card to discard pile"""
        self.plr.discardpile.set()
        card = self.game["Copper"].remove()
        self.plr.add_card(card, "discard")
        self.assertEqual(card.location, "discard")
        self.assertIsNotNone(self.plr.discardpile["Copper"])

    def test_played(self):
        """Add card to played pile"""
        self.plr.played.set()
        card = self.game["Copper"].remove()
        card.location = "played"
        self.plr.add_card(card, "played")
        self.assertIn("Copper", self.plr.played)


###############################################################################
class Test_Remove_Card(unittest.TestCase):
    """Test remove_card()"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list(0)

    def test_discard(self):
        """Remove card from discard pile"""
        self.plr.discardpile.set("Gold")
        card = self.plr.discardpile[0]
        card.location = "discard"
        self.plr.remove_card(card)
        self.assertNotIn("Gold", self.plr.discardpile)

    def test_played(self):
        """Remove card from played pile"""
        self.plr.played.set("Gold")
        card = self.plr.played[0]
        card.location = "played"
        self.plr.remove_card(card)
        self.assertNotIn("Gold", self.plr.played)


###############################################################################
class Test_Way(unittest.TestCase):
    """Test way related functions"""

    def setUp(self):
        self.game = Game.TestGame(numplayers=1, waycards=["Way of the Otter"], initcards=["Cellar"])
        self.game.start_game()
        self.plr = self.game.player_list(0)
        self.way = self.game.ways["Way of the Otter"]
        self.card = self.game["Cellar"]
        self.plr.add_card(self.card, "hand")

    def test_perform_way(self):
        """Test perform_way()"""
        self.plr.actions.set(1)
        self.assertEqual(len(self.plr.played_ways), 0)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertNotIn("Cellar", self.plr.hand)
        self.assertEqual(len(self.plr.played_ways), 1)

    def test_perform_way_no_action(self):
        """Test perform_way() with insufficient actions"""
        self.plr.actions.set(0)
        self.assertEqual(len(self.plr.played_ways), 0)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertIn("Cellar", self.plr.hand)
        self.assertEqual(len(self.plr.played_ways), 0)

    def test_relevant_way(self):
        """Is the way in the relevant cards"""
        rel = self.plr.relevant_cards()
        self.assertIn(self.way, rel)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
