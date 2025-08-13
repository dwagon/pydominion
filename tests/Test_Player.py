#!/usr/bin/env python
# pylint: disable=protected-access
"""Testing player code"""

import operator
import unittest

from dominion import Card, Game, Phase, Piles, Limits, NoCardException
from dominion.Counter import Counter


###############################################################################
class TestPlayer(unittest.TestCase):
    """Test cases for Player class"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_initialCardStacks(self) -> None:
        """Make sure initial hands are correct"""
        self.assertEqual(len(self.plr.piles[Piles.DECK]), 5)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 0)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)

    def test_initial_deck(self) -> None:
        """Ensure initial player decks are correct"""
        self.plr.piles[Piles.DECK].empty()
        self.plr._initial_deck()
        self.assertEqual(len(self.plr.piles[Piles.DECK]), 10)

    def test_deck_order(self) -> None:
        """Ensure adding cards to decks in the correct order"""
        self.plr.piles[Piles.DECK].empty()
        estate = self.game.get_card_from_pile("Estate")
        gold = self.game.get_card_from_pile("Gold")
        self.plr.add_card(estate, Piles.DECK)
        self.plr.add_card(gold, "topdeck")
        crd = self.plr.next_card()
        self.assertEqual(crd.name, "Gold")


###############################################################################
class TestTrashCard(unittest.TestCase):
    """Test plr.trash_card()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_trash_card_hand(self) -> None:
        """Test that trashing a card from hand works"""
        num_cards = self.game.count_cards()
        card = self.plr.piles[Piles.HAND][0]
        assert card is not None
        self.plr.trash_card(card)
        self.assertEqual(num_cards, self.game.count_cards())
        self.assertIn(card, self.game.trash_pile)
        self.assertNotIn(card, self.plr.piles[Piles.HAND])
        self.assertEqual(card.location, Piles.TRASH)
        self.assertEqual(card.player, None)

    def test_trash_card_played(self) -> None:
        """Test that trashing a card from played works"""
        self.plr.piles[Piles.PLAYED].set("Estate")
        num_cards = self.game.count_cards()
        card = self.plr.piles[Piles.PLAYED][0]
        assert card is not None
        self.plr.trash_card(card)
        self.assertIn(card, self.game.trash_pile)
        self.assertEqual(num_cards, self.game.count_cards())
        self.assertEqual(len(self.plr.piles[Piles.PLAYED]), 0)
        self.assertIn(card, self.plr.stats["trashed"])


###############################################################################
class TestDiscardHand(unittest.TestCase):
    """Test plr.discard_hand()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_discard(self) -> None:
        """Test discard_hand()"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver")
        self.plr.piles[Piles.PLAYED].set("Estate", "Duchy")
        self.plr.discard_hand()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 0)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 4)


###############################################################################
class TestNextCard(unittest.TestCase):
    """Test next_card()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_emptyDeck(self) -> None:
        """test empty deck"""
        self.plr.piles[Piles.DECK].empty()
        self.plr.piles[Piles.DISCARD].set("Gold")
        card = self.plr.next_card()
        self.assertEqual(card.name, "Gold")

    def test_noCards(self) -> None:
        """Test that an empty deck has no cards"""
        self.plr.piles[Piles.DECK].empty()
        self.plr.piles[Piles.DISCARD].empty()
        with self.assertRaises(NoCardException):
            self.plr.next_card()

    def test_drawOne(self) -> None:
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.piles[Piles.DISCARD].empty()
        card = self.plr.next_card()
        self.assertEqual(card.name, "Province")
        self.assertTrue(self.plr.piles[Piles.DECK].is_empty())


###############################################################################
class TestTopCard(unittest.TestCase):
    """Test top_card()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_emptyDeck(self) -> None:
        """test empty deck"""
        self.plr.piles[Piles.DECK].empty()
        self.plr.piles[Piles.DISCARD].set("Gold")
        card = self.plr.top_card()
        self.assertEqual(card.name, "Gold")

    def test_noCards(self) -> None:
        """Test that an empty deck has no cards"""
        self.plr.piles[Piles.DECK].empty()
        self.plr.piles[Piles.DISCARD].empty()
        with self.assertRaises(NoCardException):
            self.plr.top_card()

    def test_drawOne(self) -> None:
        """Test normal behaviour"""
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.piles[Piles.DISCARD].empty()
        card = self.plr.top_card()
        self.assertEqual(card.name, "Province")
        self.assertFalse(self.plr.piles[Piles.DECK].is_empty())
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])
        self.assertEqual(card.location, Piles.DECK)


###############################################################################
class TestPlayOnce(unittest.TestCase):
    """Test the play once capability"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_once(self) -> None:
        x = self.plr.do_once("test")
        self.assertTrue(x)
        x = self.plr.do_once("test")
        self.assertFalse(x)


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
class TestPlrTrashCard(unittest.TestCase):
    """Test plr_trash_card()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_none(self) -> None:
        """Trash nothing"""
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.test_input = ["0"]
        trashed = self.plr.plr_trash_card()
        self.assertEqual(trashed, [])
        self.assertNotIn("Gold", self.game.trash_pile)

    def test_two(self) -> None:
        """Trash Two cards"""
        self.plr.piles[Piles.HAND].set("Gold", "Copper", "Silver")
        self.plr.test_input = ["Gold", "Silver", "0"]
        trashed = self.plr.plr_trash_card(num=2)
        assert trashed is not None
        self.assertEqual(len(trashed), 2)
        self.assertIn("Gold", self.game.trash_pile)
        self.assertIn("Silver", self.game.trash_pile)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])

    def test_trash(self) -> None:
        """Test trashing"""
        tsize = self.game.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.test_input = ["1"]
        trashed = self.plr.plr_trash_card()
        assert trashed is not None
        self.assertEqual(trashed[0].name, "Gold")
        self.assertEqual(self.game.trash_pile.size(), tsize + 1)
        self.assertIn("Gold", self.game.trash_pile)

    def test_force(self) -> None:
        """Test trashing a card with force"""
        self.game.trash_pile.set()
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.test_input = ["0", "1"]
        trashed = self.plr.plr_trash_card(force=True)
        assert trashed is not None
        self.assertEqual(trashed[0].name, "Gold")
        self.assertEqual(self.game.trash_pile[-1].name, "Gold")
        for m in self.plr.messages:
            if "Invalid Option" in m:
                break
        else:  # pragma: no cover
            self.fail("Accepted none when force")
        for m in self.plr.messages:
            if "Trash nothing" in m:  # pragma: no cover
                self.fail("Nothing available")

    def test_exclude(self) -> None:
        """Test that the 'exclude' option works by not being able to select"""
        self.plr.piles[Piles.HAND].set("Gold", "Gold", "Copper")
        self.plr.test_input = ["1"]
        trashed = self.plr.plr_trash_card(exclude=["Gold"])
        assert trashed is not None
        self.assertEqual(trashed[0].name, "Copper")
        self.assertIn("Copper", self.game.trash_pile)

    def test_from_nothing(self) -> None:
        """Trash when there are no cards to trash"""
        self.plr.piles[Piles.HAND].set()
        trashed = self.plr.plr_trash_card()
        self.assertEqual(trashed, [])


###############################################################################
class TestPlrDiscardCard(unittest.TestCase):
    """Test the plr_discard_cards() function"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_discardNone(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["0"]
        x = self.plr.plr_discard_cards(0)
        self.assertEqual(x, [])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 4)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())

    def test_discardOne(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["1", "0"]
        x = self.plr.plr_discard_cards(1)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 3)
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 1)
        self.assertEqual(x, self.plr.piles[Piles.DISCARD]._cards)

    def test_discardAnynum(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["1", "0"]
        x = self.plr.plr_discard_cards(0, any_number=True)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 3)
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 1)
        self.assertEqual(x, self.plr.piles[Piles.DISCARD])


###############################################################################
class TestAttackVictims(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=3, initcards=["Moat"])
        self.game.start_game()
        self.plr, self.defend, self.victim = self.game.player_list()
        self.defend.piles[Piles.HAND].set("Moat")

    def test_output(self) -> None:
        v = self.plr.attack_victims()
        self.assertEqual(v, [self.victim])


###############################################################################
class TestGainCard(unittest.TestCase):
    """Test the gain_card() function"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, card_path="tests/cards", initcards=["Don't Add"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_gain_by_string(self) -> None:
        """Gain card by name"""
        self.plr.gain_card("Copper")
        top_card = self.plr.piles[Piles.DISCARD].top_card()
        assert top_card.player is not None
        self.assertEqual(top_card.name, "Copper")
        self.assertEqual(top_card.player.name, self.plr.name)

    def test_gain_by_cardpile(self) -> None:
        """Gain card by pile"""
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD].top_card().name, "Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD].top_card().player.name, self.plr.name)

    def test_gain_specific(self) -> None:
        """Gain card by specific card"""
        cu = self.game.get_card_from_pile("Copper")
        self.plr.gain_card(new_card=cu)
        self.assertEqual(self.plr.piles[Piles.DISCARD].top_card().name, "Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD].top_card().player.name, self.plr.name)

    def test_destination(self) -> None:
        """gain card to a specific destination"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.gain_card("Copper", Piles.HAND)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.plr.piles[Piles.HAND].top_card().name, "Copper")

    def test_dont_add(self) -> None:
        """Test with the DONTADD option"""
        num_cards = len(self.game.card_piles["Don't Add"])
        self.plr.gain_card("Don't Add")
        self.assertNotIn("Don't Add", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.game.card_piles["Don't Add"]), num_cards - 1)


###############################################################################
class TestSpendAllCards(unittest.TestCase):
    """Test _spend_all_cards()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_spendCards(self) -> None:
        """Spend all cards in hand"""
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Estate", "Moat")
        self.plr._spend_all_cards()
        self.assertEqual(self.plr.coins.get(), 3 + 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(len(self.plr.piles[Piles.PLAYED]), 2)
        for card in self.plr.piles[Piles.PLAYED]:
            if not card.isTreasure():  # pragma: no cover
                self.fail("Spent non treasure")


###############################################################################
class Test_pickup_card(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_pickup(self) -> None:
        """Test picking up a card"""
        self.plr.piles[Piles.DECK].set("Gold")
        self.plr.piles[Piles.HAND].set()
        self.plr.pickup_card()
        self.assertEqual(self.plr.piles[Piles.HAND][0].name, "Gold")
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)

    def test_pickup_empty(self) -> None:
        """Test picking up a card from an empty deck"""
        self.plr.piles[Piles.DECK].set()
        self.plr.piles[Piles.DISCARD].set("Gold")
        self.plr.piles[Piles.HAND].set()
        self.plr.pickup_card()
        self.assertEqual(self.plr.piles[Piles.HAND][0].name, "Gold")
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)

    def test_pick_nomore(self) -> None:
        """Test picking up a card when there isn't one to be had"""
        self.plr.piles[Piles.DECK].set()
        self.plr.piles[Piles.DISCARD].set()
        self.plr.piles[Piles.HAND].set()
        with self.assertRaises(NoCardException):
            card = self.plr.pickup_card()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)

    def test_pickups(self) -> None:
        """Test pickup_cards"""
        self.plr.piles[Piles.HAND].set()
        self.plr.pickup_cards(3, verb="test")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        count = 0
        for msg in self.plr.messages:
            if "test" in msg:
                count += 1
        self.assertEqual(count, 3)


###############################################################################
class TestMisc(unittest.TestCase):
    """Test misc functions"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Golem", "Witch", "Engineer"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_coststr(self) -> None:
        """Test coststr()"""
        witch = self.game.get_card_from_pile("Witch")
        golem = self.game.get_card_from_pile("Golem")
        eng = self.game.get_card_from_pile("Engineer")
        self.assertEqual(self.plr._cost_string(witch), "3 Coins")
        self.assertEqual(self.plr._cost_string(golem), "4 Coins, Potion")
        self.assertEqual(self.plr._cost_string(eng), "0 Coins, 4 Debt")

    def test_durationpile_size(self) -> None:
        copper = self.game.get_card_from_pile("Copper")
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
        self.plr.piles[Piles.DURATION].add(copper)
        self.plr.piles[Piles.DURATION].add(copper)
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 2)

    def test_cleanup_phase(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.cleanup_phase()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 0)


###############################################################################
class TestScore(unittest.TestCase):
    """Test score related functions"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_add_score(self) -> None:
        """Test add_score()"""
        self.plr.add_score("Bunny", 3)
        self.assertEqual(self.plr.score["Bunny"], 3)

    def test_get_score(self) -> None:
        """Test get_score()"""
        pre = self.plr.get_score()
        self.plr.piles[Piles.DISCARD].set("Province")
        self.assertEqual(self.plr.get_score(), pre + 6)

    def test_get_score_details(self) -> None:
        """Test get_score_details()"""
        self.assertEqual(self.plr.get_score_details()["Estate"], 3)
        self.plr.add_score("Bunny", 5)
        self.assertEqual(self.plr.get_score_details()["Bunny"], 5)


###############################################################################
class Test_start_turn(unittest.TestCase):
    """Test the start_turn()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_start_turn_changes(self) -> None:
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
class TestDefer(unittest.TestCase):
    """Test deferring cards"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_defer_card(self) -> None:
        """Test defer_card()"""
        moat = self.game.get_card_from_pile("Moat")
        self.plr.defer_card(moat)
        self.assertIn("Moat", self.plr.piles[Piles.DEFER])

    def test_defer_start_turn(self) -> None:
        """Make sure we run the deferpile"""
        moat = self.game.get_card_from_pile("Moat")
        self.plr.defer_card(moat)
        self.assertEqual(self.plr.actions.get(), 1)
        self.plr._defer_start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


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
        self.plr._display_overview()
        self.assertIn("| Hand: <EMPTY>", self.plr.messages)
        self.assertIn("| Played: <NONE>", self.plr.messages)

    def test_non_empty(self) -> None:
        """Test not empty hand"""
        self.plr.messages = []
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr._display_overview()
        self.assertIn("| Hand (2): Copper, Estate", self.plr.messages)
        self.assertIn("| Played (1): Moat", self.plr.messages)

    def test_reserve(self) -> None:
        """Test cards in reserve"""
        self.plr.messages = []
        self.plr.piles[Piles.RESERVE].set("Copper")
        self.plr._display_overview()
        self.assertIn("| Reserve: Copper", self.plr.messages)

    def test_duration(self) -> None:
        """Test cards in duration"""
        self.plr.messages = []
        self.plr.piles[Piles.DURATION].add(self.game.get_card_from_pile("Copper"))
        self.plr._display_overview()
        self.assertIn("| Duration: Copper", self.plr.messages)

    def test_exiled(self) -> None:
        """Test cards in exile"""
        self.plr.messages = []
        self.plr.piles[Piles.EXILE].set("Province")
        self.plr._display_overview()
        self.assertIn("| Exile: Province", self.plr.messages)

    def test_discards(self) -> None:
        """Test cards in discards"""
        self.plr.messages = []
        self.plr.piles[Piles.DISCARD].set("Copper")
        self.plr._display_overview()
        self.assertIn("| 1 cards in discard pile", self.plr.messages)

    def test_project(self) -> None:
        """Test having a project"""
        self.plr.messages = []
        self.plr.assign_project("Cathedral")
        self.plr._display_overview()
        self.assertIn("| Project: Cathedral", self.plr.messages)

    def test_artifact(self) -> None:
        """Test artifact display"""
        self.plr.messages = []
        self.plr.assign_artifact("Horn")
        self.plr._display_overview()
        self.assertIn("| Artifacts: Horn", self.plr.messages)

    def test_landmark(self) -> None:
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
class TestBuyableSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, initcards=["Moat"], badcards=["Coppersmith"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.moat = self.game.get_card_from_pile("Moat")

    def test_buy_moat(self) -> None:
        self.plr.coins.add(3)
        opts, ind = self.plr._buyable_selection(1)
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
        opts, ind = self.plr._buyable_selection(1)
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
        opts, ind = self.plr._buyable_selection(1)
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
        opts, ind = self.plr._playable_selection(1)
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
        opts, ind = self.plr._playable_selection(1)
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
        opts = self.plr._choice_selection()

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
        opts = self.plr._choice_selection()

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
        prompt = self.plr._generate_prompt()
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
        prompt = self.plr._generate_prompt()
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
        opts, idx = self.plr._night_selection(1)
        self.assertEqual(idx, 2)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0]["action"], "play")
        self.assertEqual(opts[0]["card"].name, "Monastery")

    def test_no_night(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Moat")
        opts = self.plr._night_selection(0)
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

    def test_debt(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
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
class TestBuyCard(unittest.TestCase):
    """Test buy_card()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, oldcards=True, initcards=["Embargo"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_debt(self) -> None:
        """Test buying a card when the player has a debt"""
        self.plr.debt = Counter("Debt", 1)
        self.plr.buy_card("Copper")
        self.assertIn("Must pay off debt first", self.plr.messages)

    def test_embargo(self) -> None:
        """Test buying an embargoed card"""
        self.game.card_piles["Copper"].embargo()
        self.plr.buy_card("Copper")
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Curse"])
        self.assertIn("Gained a Curse from embargo", self.plr.messages)

    def test_buy_limit(self) -> None:
        """Test setting a buy limit"""
        self.plr.coins.set(20)
        self.plr.buys.set(2)
        self.plr.limits[Limits.BUY] = 1
        self.plr.buy_card("Silver")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.buys.get(), 1)
        self.plr.buy_card("Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.buys.get(), 1)


###############################################################################
class TestSpendCoffer(unittest.TestCase):
    """Test spending coffers"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_spend_coffer(self) -> None:
        """Spend a coffer that the player has"""
        self.plr.coffers = Counter("Coffer", 1)
        self.plr.spend_coffer()
        self.assertEqual(self.plr.coffers.get(), 0)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_spendNothing(self) -> None:
        """Spend a coffer that the player doesn't have"""
        self.plr.coffers = Counter("Coffer", 0)
        self.plr.spend_coffer()
        self.assertEqual(self.plr.coffers.get(), 0)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
class TestSpendVillager(unittest.TestCase):
    """Test spend_villager()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_spend_villager(self) -> None:
        """Spend a Villager that the player has"""
        self.plr.villagers.set(1)
        self.plr.spend_villager()
        self.assertEqual(self.plr.villagers.get(), 0)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_spendNothing(self) -> None:
        """Spend a Villager that the player doesn't have"""
        self.plr.villagers.set(0)
        self.plr.spend_villager()
        self.assertEqual(self.plr.villagers.get(), 0)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
class TestPlayerGainCard(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_gain_card_equal(self) -> None:
        self.plr.test_input = ["get silver"]
        card = self.plr.plr_gain_card(3, modifier="equal")
        assert card is not None
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])
        self.assertEqual(card.name, "Silver")

    def test_gain_card_less(self) -> None:
        self.plr.test_input = ["get silver"]
        card = self.plr.plr_gain_card(4, modifier="less")
        assert card is not None
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])
        self.assertEqual(card.name, "Silver")


###############################################################################
class TestExile(unittest.TestCase):
    """Test exile pile"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_exile_card(self) -> None:
        """Test exiling a card"""
        au_card = self.game.get_card_from_pile("Gold")
        assert au_card is not None
        self.plr.piles[Piles.EXILE].empty()
        self.plr.exile_card(au_card)
        self.assertIn("Gold", self.plr.piles[Piles.EXILE])

    def test_exile_from_supply(self) -> None:
        """Test exiling a card from supply"""
        ag_size = len(self.game.card_piles["Silver"])
        self.plr.piles[Piles.EXILE].empty()
        self.plr.exile_card_from_supply("Silver")
        self.assertIn("Silver", self.plr.piles[Piles.EXILE])
        self.assertEqual(len(self.game.card_piles["Silver"]), ag_size - 1)

    def test_unexiling_card(self) -> None:
        """Test un-exiling a card"""
        self.plr.piles[Piles.EXILE].set("Gold", "Gold", "Silver")
        self.plr.test_input = ["Un-exile"]
        self.plr.gain_card("Gold")
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 3)
        self.assertEqual(len(self.plr.piles[Piles.EXILE]), 1)
        self.assertNotIn("Gold", self.plr.piles[Piles.EXILE])
        self.assertIn("Silver", self.plr.piles[Piles.EXILE])


###############################################################################
class TestPlrDiscardDownTo(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_discard_nothing(self) -> None:
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province")
        self.plr.plr_discard_down_to(3)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)

    def test_discard_one(self) -> None:
        self.plr.test_input = ["gold", "finish"]
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province", "Gold")
        self.plr.plr_discard_down_to(3)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])


###############################################################################
class TestAddCard(unittest.TestCase):
    """Test add_card()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_add(self) -> None:
        """Add card to discard pile"""
        self.plr.piles[Piles.DISCARD].set()
        card = self.game.get_card_from_pile("Copper")
        self.plr.add_card(card, Piles.DISCARD)
        self.assertEqual(card.location, Piles.DISCARD)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Copper"])

    def test_played(self) -> None:
        """Add card to played pile"""
        self.plr.piles[Piles.PLAYED].set()
        card = self.game.get_card_from_pile("Copper")
        card.location = Piles.PLAYED
        self.plr.add_card(card, "played")
        self.assertIn("Copper", self.plr.piles[Piles.PLAYED])

    def test_return_to_pile(self) -> None:
        """Test specifying a pile"""
        card = self.game.get_card_from_pile("Gold")
        gold_size = len(self.game.card_piles["Gold"])
        self.plr.add_card(card, Piles.HAND)
        self.plr.add_card(card, Piles.CARDPILE)
        self.assertEqual(len(self.game.card_piles["Gold"]), gold_size + 1)
        self.assertEqual(card.location, Piles.CARDPILE)


###############################################################################
class TestRemoveCard(unittest.TestCase):
    """Test remove_card()"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1)
        self.game.start_game()
        self.plr = self.game.player_list()[0]

    def test_discard(self) -> None:
        """Remove card from discard pile"""
        self.plr.piles[Piles.DISCARD].set("Gold")
        card = self.plr.piles[Piles.DISCARD][0]
        assert card is not None
        card.location = Piles.DISCARD
        self.plr.remove_card(card)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_played(self) -> None:
        """Remove card from played pile"""
        self.plr.piles[Piles.PLAYED].set("Gold")
        card = self.plr.piles[Piles.PLAYED][0]
        assert card is not None
        card.location = Piles.PLAYED
        self.plr.remove_card(card)
        self.assertNotIn("Gold", self.plr.piles[Piles.PLAYED])

    def test_cardpile(self) -> None:
        """Remove card from card pile"""
        pile_size = len(self.game.card_piles["Gold"])
        card = self.game.card_piles["Gold"].get_top_card()
        assert card is not None
        self.plr.remove_card(card)
        self.assertEqual(len(self.game.card_piles["Gold"]), pile_size - 1)


###############################################################################
class TestWay(unittest.TestCase):
    """Test way related functions"""

    def setUp(self) -> None:
        self.game = Game.TestGame(numplayers=1, ways=["Way of the Otter"], initcards=["Cellar"])
        self.game.start_game()
        self.plr = self.game.player_list()[0]
        self.way = self.game.ways["Way of the Otter"]
        self.card = self.game.get_card_from_pile("Cellar")
        self.plr.add_card(self.card, Piles.HAND)

    def test_perform_way(self) -> None:
        """Test perform_way()"""
        self.plr.actions.set(1)
        self.assertEqual(len(self.plr.played_ways), 0)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertNotIn("Cellar", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.played_ways), 1)

    def test_perform_way_no_action(self) -> None:
        """Test perform_way() with insufficient actions"""
        self.plr.actions.set(0)
        self.assertEqual(len(self.plr.played_ways), 0)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertIn("Cellar", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.played_ways), 0)

    def test_relevant_way(self) -> None:
        """Is the way in the relevant cards"""
        rel = self.plr.relevant_cards()
        self.assertIn(self.way, rel)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
