#!/usr/bin/env python
""" Testing player code """

import unittest
from dominion import Card
from dominion import Game


###############################################################################
class TestPlayer(unittest.TestCase):
    """Test cases for Player class"""

    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

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
        num_cards = self.g.countCards()
        card = self.plr.hand[0]
        self.plr.trash_card(card)
        self.assertEqual(num_cards, self.g.countCards())
        self.assertIsNotNone(self.g.in_trash(card))

    def test_trashcard_played(self):
        """Test that trashing a card from played works"""
        num_cards = self.g.countCards()
        self.plr.set_played("Estate")
        card = self.plr.played[0]
        self.plr.trash_card(card)
        self.assertEqual(num_cards, self.g.countCards())
        self.assertIsNotNone(self.g.in_trash(card))

    def test_deckorder(self):
        """Ensure adding cards to decks in the correct order"""
        self.plr.deck.empty()
        estate = self.g["Estate"].remove()
        gold = self.g["Gold"].remove()
        self.plr.addCard(estate, "deck")
        self.plr.addCard(gold, "topdeck")
        c = self.plr.next_card()
        self.assertEqual(c.name, "Gold")


###############################################################################
class Test_discardHand(unittest.TestCase):
    """Test plr.discardHand()"""

    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_discard(self):
        self.plr.set_hand("Copper", "Silver")
        self.plr.set_played("Estate", "Duchy")
        self.plr.discardHand()
        self.assertEqual(self.plr.hand.size(), 0)
        self.assertEqual(self.plr.played.size(), 0)
        self.assertEqual(self.plr.discardpile.size(), 4)


###############################################################################
class Test_in_played(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_emptydiscard(self):
        """Test in_played() with no played pile"""
        self.plr.set_played()
        self.assertIsNone(self.plr.in_played("Copper"))

    def test_indiscard(self):
        """Test in_played() with it the only card in the played pile"""
        self.plr.set_played("Copper")
        self.assertIsNotNone(self.plr.in_played("Copper"))

    def test_inmultidiscard(self):
        """Test in_played() with it one of many cards in the played pile"""
        self.plr.set_played("Copper", "Gold", "Copper")
        c = self.plr.in_played("Gold")
        self.assertIsNotNone(c)
        self.assertEqual(c.name, "Gold")

    def test_notinmultidiscard(self):
        """Test in_played() with it not one of many cards in the played pile"""
        self.plr.set_played("Copper", "Gold", "Copper")
        self.assertIsNone(self.plr.in_played("Estate"))


###############################################################################
class Test_in_discard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_emptydiscard(self):
        """Test in_discard() with no discard pile"""
        self.plr.set_discard()
        self.assertIsNone(self.plr.in_discard("Copper"))

    def test_indiscard(self):
        """Test in_discard() with it the only card in the discard pile"""
        self.plr.set_discard("Copper")
        self.assertIsNotNone(self.plr.in_discard("Copper"))

    def test_inmultidiscard(self):
        """Test in_discard() with it one of many cards in the discard pile"""
        self.plr.set_discard("Copper", "Gold", "Copper")
        c = self.plr.in_discard("Gold")
        self.assertIsNotNone(c)
        self.assertEqual(c.name, "Gold")

    def test_notinmultidiscard(self):
        """Test in_discard() with it not one of many cards in the discard pile"""
        self.plr.set_discard("Copper", "Gold", "Copper")
        self.assertIsNone(self.plr.in_discard("Estate"))


###############################################################################
class Test_next_card(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_emptyDeck(self):
        self.plr.deck.empty()
        self.plr.set_discard("Gold")
        c = self.plr.next_card()
        self.assertEqual(c.name, "Gold")

    def test_noCards(self):
        self.plr.deck.empty()
        self.plr.discardpile.empty()
        c = self.plr.next_card()
        self.assertIsNone(c)

    def test_drawOne(self):
        self.plr.set_deck("Province")
        self.plr.discardpile.empty()
        c = self.plr.next_card()
        self.assertEqual(c.name, "Province")
        self.assertTrue(self.plr.deck.is_empty())


###############################################################################
class Test_playonce(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_once(self):
        x = self.plr.do_once("test")
        self.assertTrue(x)
        x = self.plr.do_once("test")
        self.assertFalse(x)


###############################################################################
class Test_cardsAffordable(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
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
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_under(self):
        price = 4
        ans = self.plr.cardsUnder(price, types={Card.TYPE_ACTION: True})
        for a in ans:
            try:
                self.assertLessEqual(a.cost, price)
                self.assertTrue(a.isAction())
            except AssertionError:  # pragma: no cover
                print("a={}".format(a))
                self.g.print_state()
                raise

    def test_worth(self):
        price = 5
        ans = self.plr.cardsWorth(price, types={Card.TYPE_VICTORY: True})
        for a in ans:
            self.assertEqual(a.cost, price)
            self.assertTrue(a.isVictory())

    def test_nocost(self):
        ans = self.plr.cardsAffordable(
            "less",
            coin=None,
            potions=0,
            types={
                Card.TYPE_VICTORY: True,
                Card.TYPE_ACTION: True,
                Card.TYPE_TREASURE: True,
                Card.TYPE_NIGHT: True,
            },
        )
        self.assertIn("Province", [cp.name for cp in ans])


###############################################################################
class Test_typeSelector(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_selzero(self):
        x = self.plr.typeSelector({})
        self.assertTrue(x[Card.TYPE_ACTION])
        self.assertTrue(x[Card.TYPE_TREASURE])
        self.assertTrue(x[Card.TYPE_VICTORY])

    def test_selone(self):
        x = self.plr.typeSelector({Card.TYPE_ACTION: True})
        self.assertTrue(x[Card.TYPE_ACTION])
        self.assertFalse(x[Card.TYPE_TREASURE])
        self.assertFalse(x[Card.TYPE_VICTORY])

    def test_seltwo(self):
        x = self.plr.typeSelector({Card.TYPE_ACTION: True, Card.TYPE_VICTORY: True})
        self.assertTrue(x[Card.TYPE_ACTION])
        self.assertFalse(x[Card.TYPE_TREASURE])
        self.assertTrue(x[Card.TYPE_VICTORY])


###############################################################################
class Test_plrTrashCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_None(self):
        self.plr.set_hand("Gold")
        self.plr.test_input = ["0"]
        x = self.plr.plrTrashCard()
        self.assertEqual(x, [])
        self.assertIsNone(self.g.in_trash("Gold"))

    def test_Two(self):
        self.plr.set_hand("Gold", "Copper", "Silver")
        self.plr.test_input = ["Gold", "Silver", "0"]
        x = self.plr.plrTrashCard(num=2)
        self.assertEqual(len(x), 2)
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertIsNotNone(self.g.in_trash("Silver"))
        self.assertIsNotNone(self.plr.in_hand("Copper"))

    def test_Trash(self):
        tsize = self.g.trashSize()
        self.plr.set_hand("Gold")
        self.plr.test_input = ["1"]
        x = self.plr.plrTrashCard()
        self.assertEqual(x[0].name, "Gold")
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIn("Gold", [_.name for _ in self.g.trashpile])

    def test_Force(self):
        self.plr.set_hand("Gold")
        self.plr.test_input = ["0", "1"]
        x = self.plr.plrTrashCard(force=True)
        self.assertEqual(x[0].name, "Gold")
        self.assertEqual(self.g.trashpile[-1].name, "Gold")
        for m in self.plr.messages:
            if "Invalid Option" in m:
                break
        else:  # pragma: no cover
            self.fail("Accepted none when force")
        for m in self.plr.messages:
            if "Trash nothing" in m:  # pragma: no cover
                self.fail("Nothing available")

    def test_exclude(self):
        self.plr.set_hand("Gold", "Gold", "Copper")
        self.plr.test_input = ["1"]
        x = self.plr.plrTrashCard(exclude=["Gold"])
        self.assertEqual(x[0].name, "Copper")
        self.assertEqual(self.g.trashpile[-1].name, "Copper")


###############################################################################
class Test_plrDiscardCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_discardNone(self):
        self.plr.set_hand("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["0"]
        x = self.plr.plrDiscardCards(0)
        self.assertEqual(x, [])
        self.assertEqual(len(self.plr.hand), 4)
        self.assertTrue(self.plr.discardpile.is_empty())

    def test_discardOne(self):
        self.plr.set_hand("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["1", "0"]
        x = self.plr.plrDiscardCards(1)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile.cards)

    def test_discardAnynum(self):
        self.plr.set_hand("Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["1", "0"]
        x = self.plr.plrDiscardCards(0, anynum=True)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile)


###############################################################################
class Test_attackVictims(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=3, initcards=["Moat"])
        self.g.start_game()
        self.plr, self.defend, self.victim = self.g.player_list()
        self.defend.set_hand("Moat")

    def test_output(self):
        v = self.plr.attackVictims()
        self.assertEqual(v, [self.victim])


###############################################################################
class Test_in_deck(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_indeck(self):
        """Test card is in deck"""
        self.plr.set_deck("Copper")
        self.assertTrue(self.plr.in_deck("Copper"))
        self.assertEqual(self.plr.in_deck("Copper").name, "Copper")

    def test_notindeck(self):
        """Test card that isn't in deck"""
        self.plr.set_deck("Copper")
        self.assertFalse(self.plr.in_deck("Estate"))


###############################################################################
class Test_in_hand(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_inhand(self):
        """Test card is in hand"""
        self.plr.set_hand("Copper")
        self.assertTrue(self.plr.in_hand("Copper"))
        self.assertEqual(self.plr.in_hand("Copper").name, "Copper")

    def test_notinhand(self):
        """Test card that isn't in hand"""
        self.plr.set_hand("Copper")
        self.assertFalse(self.plr.in_hand("Estate"))


###############################################################################
class Test_gainCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_gainByString(self):
        self.plr.gainCard("Copper")
        self.assertEqual(self.plr.discardpile[0].name, "Copper")

    def test_gainByCardpile(self):
        cp = self.g["Copper"]
        self.plr.gainCard(cp)
        self.assertEqual(self.plr.discardpile[0].name, "Copper")

    def test_gainSpecific(self):
        cu = self.g["Copper"].remove()
        self.plr.gainCard(newcard=cu)
        self.assertEqual(self.plr.discardpile[0].name, "Copper")

    def test_destination(self):
        self.plr.hand.empty()
        self.plr.gainCard("Copper", "hand")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand[0].name, "Copper")


###############################################################################
class Test_spendAllCards(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_spendCards(self):
        """Spend all cards in hand"""
        self.plr.set_hand("Gold", "Silver", "Estate", "Moat")
        self.plr.spendAllCards()
        self.assertEqual(self.plr.getCoin(), 3 + 2)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(len(self.plr.played), 2)
        for c in self.plr.played:
            if not c.isTreasure():  # pragma: no cover
                self.fail("Spent non treasure")


###############################################################################
class Test_pickup_card(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_pickup(self):
        """Test picking up a card"""
        self.plr.set_deck("Gold")
        self.plr.set_hand()
        self.plr.pickup_card()
        self.assertEqual(self.plr.hand[0].name, "Gold")
        self.assertEqual(self.plr.deck.size(), 0)
        self.assertEqual(self.plr.hand.size(), 1)

    def test_pickup_empty(self):
        """Test picking up a card from an empty deck"""
        self.plr.set_deck()
        self.plr.set_discard("Gold")
        self.plr.set_hand()
        self.plr.pickup_card()
        self.assertEqual(self.plr.hand[0].name, "Gold")
        self.assertEqual(self.plr.deck.size(), 0)
        self.assertEqual(self.plr.hand.size(), 1)

    def test_pick_nomore(self):
        """Test picking up a card when there isn't one to be had"""
        self.plr.set_deck()
        self.plr.set_discard()
        self.plr.set_hand()
        c = self.plr.pickup_card()
        self.assertIsNone(c)
        self.assertEqual(self.plr.hand.size(), 0)

    def test_pickups(self):
        """Test pickup_cards"""
        self.plr.set_hand()
        self.plr.pickup_cards(3, verb="test")
        self.assertEqual(self.plr.hand.size(), 3)
        count = 0
        for msg in self.plr.messages:
            if "test" in msg:
                count += 1
        self.assertEqual(count, 3)


###############################################################################
class Test_misc(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Golem", "Witch", "Engineer"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_set_played(self):
        self.plr.set_played("Silver", "Copper")
        self.assertEqual(self.plr.played.size(), 2)

    def test_set_played_empty(self):
        self.plr.set_played()
        self.assertEqual(self.plr.played.size(), 0)

    def test_set_discard(self):
        self.plr.set_discard("Silver", "Copper")
        self.assertEqual(self.plr.discardpile.size(), 2)

    def test_set_hand(self):
        self.plr.set_hand("Silver", "Copper")
        self.assertEqual(self.plr.hand.size(), 2)

    def test_set_deck(self):
        self.plr.set_deck("Silver", "Copper")
        self.assertEqual(self.plr.deck.size(), 2)

    def test_get_actions(self):
        self.plr.actions = 3
        numactions = self.plr.get_actions()
        self.assertEqual(numactions, 3)

    def test_addActions(self):
        self.plr.actions = 3
        self.plr.addActions(2)
        self.assertEqual(self.plr.actions, 5)

    def test_get_buys(self):
        self.plr.buys = 3
        numbuys = self.plr.get_buys()
        self.assertEqual(numbuys, 3)

    def test_addBuys(self):
        self.plr.buys = 3
        self.plr.addBuys(2)
        self.assertEqual(self.plr.buys, 5)

    def test_coststr(self):
        witch = self.g["Witch"].remove()
        golem = self.g["Golem"].remove()
        eng = self.g["Engineer"].remove()
        self.assertEqual(self.plr.coststr(witch), "3 Coins")
        self.assertEqual(self.plr.coststr(golem), "4 Coins, Potion")
        self.assertEqual(self.plr.coststr(eng), "0 Coins, 4 Debt")

    def test_in_hand(self):
        self.plr.set_hand("Silver")
        self.assertFalse(self.plr.in_hand("Gold"))
        self.assertTrue(self.plr.in_hand("Silver"))

    def test_getPotions(self):
        self.plr.potions = 3
        self.assertEqual(self.plr.getPotions(), 3)

    def test_durationpile_size(self):
        copper = self.g["Copper"].remove()
        self.assertEqual(self.plr.durationpile.size(), 0)
        self.plr.durationpile.add(copper)
        self.plr.durationpile.add(copper)
        self.assertEqual(self.plr.durationpile.size(), 2)

    def test_cleanup_phase(self):
        self.plr.set_hand("Copper")
        self.plr.cleanup_phase()
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.played.size(), 0)


###############################################################################
class Test_displayOverview(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Moat"], initprojects=["Cathedral"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_empty(self):
        self.plr.messages = []
        self.plr.set_hand()
        self.plr.set_played()
        self.plr.displayOverview()
        self.assertIn("| Hand: <EMPTY>", self.plr.messages)
        self.assertIn("| Played: <NONE>", self.plr.messages)

    def test_non_empty(self):
        self.plr.messages = []
        self.plr.set_hand("Copper", "Estate")
        self.plr.set_played("Moat")
        self.plr.displayOverview()
        self.assertIn("| Hand: Copper, Estate", self.plr.messages)
        self.assertIn("| Played: Moat", self.plr.messages)

    def test_reserve(self):
        self.plr.messages = []
        self.plr.set_reserve("Copper")
        self.plr.displayOverview()
        self.assertIn("| Reserve: Copper", self.plr.messages)

    def test_duration(self):
        self.plr.messages = []
        self.plr.durationpile.add(self.g["Copper"].remove())
        self.plr.displayOverview()
        self.assertIn("| Duration: Copper", self.plr.messages)

    def test_discards(self):
        self.plr.messages = []
        self.plr.set_discard("Copper")
        self.plr.displayOverview()
        self.assertIn("| 1 cards in discard pile", self.plr.messages)

    def test_project(self):
        self.plr.messages = []
        self.plr.assign_project("Cathedral")
        self.plr.displayOverview()
        self.assertIn("| Project: Cathedral", self.plr.messages)

    def test_artifact(self):
        self.plr.messages = []
        self.plr.assign_artifact("Horn")
        self.plr.displayOverview()
        self.assertIn("| Artifacts: Horn", self.plr.messages)


###############################################################################
class Test_buyable_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Moat"], badcards=["Coppersmith"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g["Moat"].remove()

    def test_buy_moat(self):
        self.plr.addCoin(3)
        opts, ind = self.plr.buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"] == "Moat":
                self.assertEqual(i["verb"], "Buy")
                self.assertEqual(i[Card.TYPE_ACTION], "buy")
                self.assertEqual(i["card"], self.g["Moat"])
                break
        else:  # pragma: no coverage
            self.fail("Moat not buyable")

    def test_buy_copper(self):
        self.plr.coin = 0
        opts, ind = self.plr.buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"].startswith("Copper"):
                try:
                    self.assertEqual(i[Card.TYPE_ACTION], "buy")
                    self.assertEqual(i["card"], self.g["Copper"])
                except AssertionError:  # pragma: no cover
                    print("Buy Copper {}".format(i))
                    self.g.print_state()
                    raise
                break
        else:  # pragma: no coverage
            self.fail("Copper not buyable")

    def test_buy_token(self):
        self.plr.addCoin(2)
        self.plr.place_token("+1 Card", "Moat")
        opts, ind = self.plr.buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i["name"] == "Moat":
                self.assertIn("[Tkn: +1 Card]", i["details"])
                break
        else:  # pragma: no coverage
            self.fail("Moat not buyable")


###############################################################################
class Test_playable_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g["Moat"].remove()

    def test_play(self):
        self.plr.addCard(self.moat, "hand")
        opts, ind = self.plr.playable_selection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.moat)
        self.assertEqual(opts[0]["desc"], "+2 cards, defense")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0]["name"], "Moat")
        self.assertEqual(ind, 2)

    def test_token(self):
        self.plr.place_token("+1 Card", "Moat")
        self.plr.addCard(self.moat, "hand")
        opts, ind = self.plr.playable_selection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["card"], self.moat)
        self.assertTrue("[Tkn: +1 Card]" in opts[0]["notes"])
        self.assertEqual(ind, 2)


###############################################################################
class Test_choice_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Moat", "Alchemist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g["Moat"].remove()
        self.potion = self.g["Potion"].remove()

    def test_action_phase(self):
        self.plr.set_hand("Moat")
        self.plr.phase = Card.TYPE_ACTION
        opts, _ = self.plr.choice_selection()

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0][Card.TYPE_ACTION], "quit")
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["verb"], "Play")
        self.assertEqual(opts[1]["name"], "Moat")
        self.assertEqual(opts[1][Card.TYPE_ACTION], "play")
        self.assertEqual(opts[1]["selector"], "a")

        self.assertEqual(len(opts), 2)

    def test_buy_phase(self):
        self.plr.set_hand("Copper")
        self.plr.phase = "buy"
        self.plr.coffer = 0  # Stop card choice_selection breaking test
        opts, _ = self.plr.choice_selection()

        self.assertEqual(opts[0]["verb"], "End Phase")
        self.assertEqual(opts[0][Card.TYPE_ACTION], "quit")
        self.assertEqual(opts[0]["selector"], "0")
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1][Card.TYPE_ACTION], "spendall")
        self.assertEqual(opts[2][Card.TYPE_ACTION], "spend")

    def test_prompt(self):
        self.plr.actions = 3
        self.plr.buys = 7
        self.plr.potions = 9
        self.plr.coin = 5
        self.plr.coffer = 1
        self.plr.phase = "buy"
        self.plr.debt = 2
        _, prompt = self.plr.choice_selection()
        self.assertIn("Actions=3", prompt)
        self.assertIn("Coins=5", prompt)
        self.assertIn("Buys=7", prompt)
        self.assertIn("Debt=2", prompt)
        self.assertIn("Potion", prompt)
        self.assertIn("Coffer=1", prompt)

    def test_nothing_prompt(self):
        self.plr.actions = 0
        self.plr.buys = 0
        self.plr.potions = 0
        self.plr.coin = 0
        self.plr.coffer = 0
        self.plr.phase = "buy"
        _, prompt = self.plr.choice_selection()
        self.assertIn("Actions=0", prompt)
        self.assertIn("Buys=0", prompt)
        self.assertNotIn("Coins", prompt)
        self.assertNotIn("Potions", prompt)
        self.assertNotIn("Coffer", prompt)


###############################################################################
class Test_night_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Monastery", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g["Moat"].remove()

    def test_play(self):
        self.plr.set_hand("Copper", "Moat", "Monastery")
        opts, idx = self.plr.night_selection(1)
        self.assertEqual(idx, 2)
        self.assertEqual(opts[0]["selector"], "b")
        self.assertEqual(opts[0]["verb"], "Play")
        self.assertEqual(opts[0][Card.TYPE_ACTION], "play")
        self.assertEqual(opts[0]["card"].name, "Monastery")

    def test_no_night(self):
        self.plr.set_hand("Copper", "Moat")
        opts = self.plr.night_selection(0)
        self.assertEqual(opts, ([], 0))


###############################################################################
class Test_spendable_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            initcards=["Moat", "Alchemist"],
            badcards=["Baker"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g["Moat"].remove()
        self.potion = self.g["Potion"].remove()

    def test_play(self):
        self.plr.set_hand("Copper", "Estate")
        self.plr.addCard(self.potion, "hand")
        self.plr.addCard(self.moat, "hand")
        self.plr.gainCoffer(1)
        self.plr.gainVillager(1)
        opts = self.plr.spendable_selection()
        self.assertEqual(opts[0]["selector"], "1")
        self.assertEqual(opts[0][Card.TYPE_ACTION], "spendall")
        self.assertIn("Spend all treasures", opts[0]["verb"])
        self.assertIsNone(opts[0]["card"])

        self.assertEqual(opts[1]["selector"], "2")
        self.assertEqual(opts[1]["verb"], "Spend Coffer (1 coin)")
        self.assertEqual(opts[1][Card.TYPE_ACTION], "coffer")
        self.assertIsNone(opts[1]["card"])

        self.assertEqual(opts[2]["selector"], "4")
        self.assertEqual(opts[2]["verb"], "Spend")
        self.assertEqual(opts[2]["name"], "Copper")
        self.assertEqual(opts[2][Card.TYPE_ACTION], "spend")
        self.assertEqual(opts[2]["card"].name, "Copper")

        self.assertEqual(opts[3]["verb"], "Spend")
        self.assertEqual(opts[3]["selector"], "5")
        self.assertEqual(opts[3][Card.TYPE_ACTION], "spend")
        self.assertEqual(opts[3]["card"].name, "Potion")

    def test_debt(self):
        self.plr.set_hand("Copper")
        self.plr.debt = 1
        self.plr.coin = 1
        self.plr.coffer = 0
        try:
            opts = self.plr.spendable_selection()
            self.assertEqual(opts[1]["selector"], "3")
            self.assertEqual(opts[1][Card.TYPE_ACTION], "payback")
            self.assertEqual(opts[1]["verb"], "Payback Debt")
            self.assertIsNone(opts[1]["card"])
        except AssertionError:  # pragma: no cover
            print("debt")
            self.g.print_state()
            raise


###############################################################################
class Test_buyCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Embargo"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_debt(self):
        self.plr.debt = 1
        self.plr.buyCard(self.g["Copper"])
        self.assertIn("Must pay off debt first", self.plr.messages)

    def test_embargo(self):
        self.g["Copper"].embargo()
        self.plr.buyCard(self.g["Copper"])
        self.assertIsNotNone(self.plr.in_discard("Curse"))
        self.assertIn("Gained a Curse from embargo", self.plr.messages)


###############################################################################
class Test_spendCoffer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_spendCoffer(self):
        """Spend a coffer that the player has"""
        self.plr.coffer = 1
        self.plr.spendCoffer()
        self.assertEqual(self.plr.getCoffer(), 0)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_spendNothing(self):
        """Spend a coffer that the player doesn't have"""
        self.plr.coffer = 0
        self.plr.spendCoffer()
        self.assertEqual(self.plr.getCoffer(), 0)
        self.assertEqual(self.plr.getCoin(), 0)


###############################################################################
class Test_spendVillager(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_spendVillager(self):
        """Spend a Villager that the player has"""
        self.plr.villager = 1
        self.plr.spendVillager()
        self.assertEqual(self.plr.getVillager(), 0)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_spendNothing(self):
        """Spend a Villager that the player doesn't have"""
        self.plr.villager = 0
        self.plr.spendVillager()
        self.assertEqual(self.plr.getVillager(), 0)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
class Test_plrGainCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_gainCard_equal(self):
        self.plr.test_input = ["get silver"]
        c = self.plr.plrGainCard(3, modifier="equal")
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertEqual(c.name, "Silver")

    def test_gainCard_less(self):
        self.plr.test_input = ["get silver"]
        c = self.plr.plrGainCard(4, modifier="less")
        self.assertIsNotNone(self.plr.in_discard("Silver"))
        self.assertEqual(c.name, "Silver")


###############################################################################
class Test_exile(unittest.TestCase):
    """Test exile pile"""

    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_in_exile(self):
        self.plr.set_exile("Silver")
        self.assertIsNotNone(self.plr.in_exile("Silver"))

    def test_exile_card(self):
        au_card = self.g["Gold"].remove()
        self.plr.set_exile()
        self.plr.exile_card(au_card)
        self.assertIsNotNone(self.plr.in_exile("Gold"))


###############################################################################
class Test_plrDiscardDownTo(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_discard_nothing(self):
        self.plr.set_hand("Estate", "Duchy", "Province")
        self.plr.plrDiscardDownTo(3)
        self.assertEqual(self.plr.discardpile.size(), 0)

    def test_discard_one(self):
        self.plr.test_input = ["gold", "finish"]
        self.plr.set_hand("Estate", "Duchy", "Province", "Gold")
        self.plr.plrDiscardDownTo(3)
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertIsNotNone(self.plr.in_discard("Gold"))


###############################################################################
class Test_Favor(unittest.TestCase):
    """Favor testing"""

    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_setfavor(self):
        """plr.setFavor()"""
        self.plr.favors = 0
        self.plr.setFavor(3)
        self.assertEqual(self.plr.favors, 3)

    def test_addfavor(self):
        """plr.addFavor()"""
        self.plr.favors = 0
        self.plr.addFavor()
        self.assertEqual(self.plr.favors, 1)
        self.plr.addFavor(1)
        self.assertEqual(self.plr.favors, 2)

    def test_getfavor(self):
        """plr.getFavor()"""
        self.plr.favors = 3
        self.assertEqual(self.plr.getFavor(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
