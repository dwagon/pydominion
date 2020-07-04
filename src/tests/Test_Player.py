#!/usr/bin/env python

import unittest
import Game


###############################################################################
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_initialCardStacks(self):
        """ Make sure initial hands are correct """
        self.assertEqual(len(self.plr.deck), 5)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.playedSize(), 0)
        self.assertEqual(self.plr.discardSize(), 0)

    def test_initialDeck(self):
        """ Ensure initial player decks are correct """
        self.plr.deck.empty()
        self.plr.initial_Deck(heirlooms=[])
        self.assertEqual(len(self.plr.deck), 10)

    def test_trashcard_hand(self):
        """ Test that trashing a card from hand works """
        num_cards = self.g.countCards()
        card = self.plr.hand[0]
        self.plr.trashCard(card)
        self.assertEqual(num_cards, self.g.countCards())
        self.assertIsNotNone(self.g.in_trash(card))

    def test_trashcard_played(self):
        """ Test that trashing a card from played works """
        num_cards = self.g.countCards()
        self.plr.setPlayed('Estate')
        card = self.plr.played[0]
        self.plr.trashCard(card)
        self.assertEqual(num_cards, self.g.countCards())
        self.assertIsNotNone(self.g.in_trash(card))

    def test_deckorder(self):
        """ Ensure adding cards to decks in the correct order """
        self.plr.deck.empty()
        estate = self.g['Estate'].remove()
        gold = self.g['Gold'].remove()
        self.plr.addCard(estate, 'deck')
        self.plr.addCard(gold, 'topdeck')
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Gold')


###############################################################################
class Test_discardHand(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_discard(self):
        self.plr.setHand('Copper', 'Silver')
        self.plr.setPlayed('Estate', 'Duchy')
        self.plr.discardHand()
        self.assertEqual(self.plr.handSize(), 0)
        self.assertEqual(self.plr.playedSize(), 0)
        self.assertEqual(self.plr.discardSize(), 4)


###############################################################################
class Test_inPlayed(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_emptydiscard(self):
        """ Test inPlayed() with no played pile """
        self.plr.setPlayed()
        self.assertIsNone(self.plr.inPlayed('Copper'))

    def test_indiscard(self):
        """ Test inPlayed() with it the only card in the played pile """
        self.plr.setPlayed('Copper')
        self.assertIsNotNone(self.plr.inPlayed('Copper'))

    def test_inmultidiscard(self):
        """ Test inPlayed() with it one of many cards in the played pile """
        self.plr.setPlayed('Copper', 'Gold', 'Copper')
        c = self.plr.inPlayed('Gold')
        self.assertIsNotNone(c)
        self.assertEqual(c.name, 'Gold')

    def test_notinmultidiscard(self):
        """ Test inPlayed() with it not one of many cards in the played pile """
        self.plr.setPlayed('Copper', 'Gold', 'Copper')
        self.assertIsNone(self.plr.inPlayed('Estate'))


###############################################################################
class Test_inDiscard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_emptydiscard(self):
        """ Test inDiscard() with no discard pile """
        self.plr.setDiscard()
        self.assertIsNone(self.plr.inDiscard('Copper'))

    def test_indiscard(self):
        """ Test inDiscard() with it the only card in the discard pile """
        self.plr.setDiscard('Copper')
        self.assertIsNotNone(self.plr.inDiscard('Copper'))

    def test_inmultidiscard(self):
        """ Test inDiscard() with it one of many cards in the discard pile """
        self.plr.setDiscard('Copper', 'Gold', 'Copper')
        c = self.plr.inDiscard('Gold')
        self.assertIsNotNone(c)
        self.assertEqual(c.name, 'Gold')

    def test_notinmultidiscard(self):
        """ Test inDiscard() with it not one of many cards in the discard pile """
        self.plr.setDiscard('Copper', 'Gold', 'Copper')
        self.assertIsNone(self.plr.inDiscard('Estate'))


###############################################################################
class Test_nextCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_emptyDeck(self):
        self.plr.deck.empty()
        self.plr.setDiscard('Gold')
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Gold')

    def test_noCards(self):
        self.plr.deck.empty()
        self.plr.discardpile.empty()
        c = self.plr.nextCard()
        self.assertIsNone(c)

    def test_drawOne(self):
        self.plr.setDeck('Province')
        self.plr.discardpile.empty()
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Province')
        self.assertTrue(self.plr.deck.isEmpty())


###############################################################################
class Test_playonce(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_once(self):
        x = self.plr.do_once('test')
        self.assertTrue(x)
        x = self.plr.do_once('test')
        self.assertFalse(x)


###############################################################################
class Test_cardsAffordable(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_under(self):
        price = 4
        ans = self.plr.cardsUnder(price, types={'action': True})
        for a in ans:
            try:
                self.assertLessEqual(a.cost, price)
                self.assertTrue(a.isAction())
            except AssertionError:      # pragma: no cover
                print("a={}".format(a))
                self.g.print_state()
                raise

    def test_worth(self):
        price = 5
        ans = self.plr.cardsWorth(price, types={'victory': True})
        for a in ans:
            self.assertEqual(a.cost, price)
            self.assertTrue(a.isVictory())

    def test_nocost(self):
        ans = self.plr.cardsAffordable(
            'less', coin=None, potions=0,
            types={'victory': True, 'action': True, 'treasure': True, 'night': True}
        )
        self.assertIn('Province', [cp.name for cp in ans])


###############################################################################
class Test_typeSelector(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_selzero(self):
        x = self.plr.typeSelector({})
        self.assertTrue(x['action'])
        self.assertTrue(x['treasure'])
        self.assertTrue(x['victory'])

    def test_selone(self):
        x = self.plr.typeSelector({'action': True})
        self.assertTrue(x['action'])
        self.assertFalse(x['treasure'])
        self.assertFalse(x['victory'])

    def test_seltwo(self):
        x = self.plr.typeSelector({'action': True, 'victory': True})
        self.assertTrue(x['action'])
        self.assertFalse(x['treasure'])
        self.assertTrue(x['victory'])


###############################################################################
class Test_plrTrashCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_None(self):
        self.plr.setHand('Gold')
        self.plr.test_input = ['0']
        x = self.plr.plrTrashCard()
        self.assertEqual(x, [])
        self.assertIsNone(self.g.in_trash('Gold'))

    def test_Two(self):
        self.plr.setHand('Gold', 'Copper', 'Silver')
        self.plr.test_input = ['Gold', 'Silver', '0']
        x = self.plr.plrTrashCard(num=2)
        self.assertEqual(len(x), 2)
        self.assertIsNotNone(self.g.in_trash('Gold'))
        self.assertIsNotNone(self.g.in_trash('Silver'))
        self.assertIsNotNone(self.plr.inHand('Copper'))

    def test_Trash(self):
        tsize = self.g.trashSize()
        self.plr.setHand('Gold')
        self.plr.test_input = ['1']
        x = self.plr.plrTrashCard()
        self.assertEqual(x[0].name, 'Gold')
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIn('Gold', [_.name for _ in self.g.trashpile])

    def test_Force(self):
        self.plr.setHand('Gold')
        self.plr.test_input = ['0', '1']
        x = self.plr.plrTrashCard(force=True)
        self.assertEqual(x[0].name, 'Gold')
        self.assertEqual(self.g.trashpile[-1].name, 'Gold')
        for m in self.plr.messages:
            if 'Invalid Option' in m:
                break
        else:   # pragma: no cover
            self.fail("Accepted none when force")
        for m in self.plr.messages:
            if 'Trash nothing' in m:    # pragma: no cover
                self.fail("Nothing available")

    def test_exclude(self):
        self.plr.setHand('Gold', 'Gold', 'Copper')
        self.plr.test_input = ['1']
        x = self.plr.plrTrashCard(exclude=['Gold'])
        self.assertEqual(x[0].name, 'Copper')
        self.assertEqual(self.g.trashpile[-1].name, 'Copper')


###############################################################################
class Test_plrDiscardCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_discardNone(self):
        self.plr.setHand('Copper', 'Estate', 'Province', 'Gold')
        self.plr.test_input = ['0']
        x = self.plr.plrDiscardCards(0)
        self.assertEqual(x, [])
        self.assertEqual(len(self.plr.hand), 4)
        self.assertTrue(self.plr.discardpile.isEmpty())

    def test_discardOne(self):
        self.plr.setHand('Copper', 'Estate', 'Province', 'Gold')
        self.plr.test_input = ['1', '0']
        x = self.plr.plrDiscardCards(1)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile.cards)

    def test_discardAnynum(self):
        self.plr.setHand('Copper', 'Estate', 'Province', 'Gold')
        self.plr.test_input = ['1', '0']
        x = self.plr.plrDiscardCards(0, anynum=True)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile)


###############################################################################
class Test_attackVictims(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=3, initcards=['Moat'])
        self.g.start_game()
        self.plr, self.defend, self.victim = self.g.player_list()
        self.defend.setHand('Moat')

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
        """ Test card is in deck """
        self.plr.setDeck('Copper')
        self.assertTrue(self.plr.in_deck('Copper'))
        self.assertEqual(self.plr.in_deck('Copper').name, 'Copper')

    def test_notindeck(self):
        """ Test card that isn't in deck """
        self.plr.setDeck('Copper')
        self.assertFalse(self.plr.in_deck('Estate'))


###############################################################################
class Test_inHand(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_inhand(self):
        """ Test card is in hand """
        self.plr.setHand('Copper')
        self.assertTrue(self.plr.inHand('Copper'))
        self.assertEqual(self.plr.inHand('Copper').name, 'Copper')

    def test_notinhand(self):
        """ Test card that isn't in hand """
        self.plr.setHand('Copper')
        self.assertFalse(self.plr.inHand('Estate'))


###############################################################################
class Test_gainCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_gainByString(self):
        self.plr.gainCard('Copper')
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')

    def test_gainByCardpile(self):
        cp = self.g['Copper']
        self.plr.gainCard(cp)
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')

    def test_gainSpecific(self):
        cu = self.g['Copper'].remove()
        self.plr.gainCard(newcard=cu)
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')

    def test_destination(self):
        self.plr.hand.empty()
        self.plr.gainCard('Copper', 'hand')
        self.assertTrue(self.plr.discardpile.isEmpty())
        self.assertEqual(self.plr.hand[0].name, 'Copper')


###############################################################################
class Test_spendAllCards(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_spendCards(self):
        """ Spend all cards in hand"""
        self.plr.setHand('Gold', 'Silver', 'Estate', 'Moat')
        self.plr.spendAllCards()
        self.assertEqual(self.plr.getCoin(), 3 + 2)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(len(self.plr.played), 2)
        for c in self.plr.played:
            if not c.isTreasure():  # pragma: no cover
                self.fail("Spent non treasure")


###############################################################################
class Test_pickupCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_pickup(self):
        """ Test picking up a card """
        self.plr.setDeck('Gold')
        self.plr.setHand()
        self.plr.pickupCard()
        self.assertEqual(self.plr.hand[0].name, 'Gold')
        self.assertEqual(self.plr.deckSize(), 0)
        self.assertEqual(self.plr.handSize(), 1)

    def test_pickup_empty(self):
        """ Test picking up a card from an empty deck"""
        self.plr.setDeck()
        self.plr.setDiscard('Gold')
        self.plr.setHand()
        self.plr.pickupCard()
        self.assertEqual(self.plr.hand[0].name, 'Gold')
        self.assertEqual(self.plr.deckSize(), 0)
        self.assertEqual(self.plr.handSize(), 1)

    def test_pick_nomore(self):
        """ Test picking up a card when there isn't one to be had """
        self.plr.setDeck()
        self.plr.setDiscard()
        self.plr.setHand()
        c = self.plr.pickupCard()
        self.assertIsNone(c)
        self.assertEqual(self.plr.handSize(), 0)

    def test_pickups(self):
        """ Test pickupCards """
        self.plr.setHand()
        self.plr.pickupCards(3, verb='test')
        self.assertEqual(self.plr.handSize(), 3)
        count = 0
        for msg in self.plr.messages:
            if 'test' in msg:
                count += 1
        self.assertEqual(count, 3)


###############################################################################
class Test_misc(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Golem', 'Witch', 'Engineer'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_setPlayed(self):
        self.plr.setPlayed('Silver', 'Copper')
        self.assertEqual(self.plr.playedSize(), 2)

    def test_setPlayed_empty(self):
        self.plr.setPlayed()
        self.assertEqual(self.plr.playedSize(), 0)

    def test_setDiscard(self):
        self.plr.setDiscard('Silver', 'Copper')
        self.assertEqual(self.plr.discardSize(), 2)

    def test_setHand(self):
        self.plr.setHand('Silver', 'Copper')
        self.assertEqual(self.plr.handSize(), 2)

    def test_setDeck(self):
        self.plr.setDeck('Silver', 'Copper')
        self.assertEqual(self.plr.deckSize(), 2)

    def test_getActions(self):
        self.plr.actions = 3
        numactions = self.plr.getActions()
        self.assertEqual(numactions, 3)

    def test_addActions(self):
        self.plr.actions = 3
        self.plr.addActions(2)
        self.assertEqual(self.plr.actions, 5)

    def test_getBuys(self):
        self.plr.buys = 3
        numbuys = self.plr.getBuys()
        self.assertEqual(numbuys, 3)

    def test_addBuys(self):
        self.plr.buys = 3
        self.plr.addBuys(2)
        self.assertEqual(self.plr.buys, 5)

    def test_coststr(self):
        witch = self.g['Witch'].remove()
        golem = self.g['Golem'].remove()
        eng = self.g['Engineer'].remove()
        self.assertEqual(self.plr.coststr(witch), "3 Coins")
        self.assertEqual(self.plr.coststr(golem), "4 Coins, Potion")
        self.assertEqual(self.plr.coststr(eng), "0 Coins, 4 Debt")

    def test_inHand(self):
        self.plr.setHand('Silver')
        self.assertFalse(self.plr.inHand('Gold'))
        self.assertTrue(self.plr.inHand('Silver'))

    def test_getPotions(self):
        self.plr.potions = 3
        self.assertEqual(self.plr.getPotions(), 3)

    def test_durationSize(self):
        copper = self.g['Copper'].remove()
        self.assertEqual(self.plr.durationSize(), 0)
        self.plr.durationpile.add(copper)
        self.plr.durationpile.add(copper)
        self.assertEqual(self.plr.durationSize(), 2)

    def test_cleanup_phase(self):
        self.plr.setHand('Copper')
        self.plr.cleanup_phase()
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.playedSize(), 0)


###############################################################################
class Test_displayOverview(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'], initprojects=['Cathedral'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_empty(self):
        self.plr.messages = []
        self.plr.setHand()
        self.plr.setPlayed()
        self.plr.displayOverview()
        self.assertIn('| Hand: <EMPTY>', self.plr.messages)
        self.assertIn('| Played: <NONE>', self.plr.messages)

    def test_non_empty(self):
        self.plr.messages = []
        self.plr.setHand('Copper', 'Estate')
        self.plr.setPlayed('Moat')
        self.plr.displayOverview()
        self.assertIn('| Hand: Copper, Estate', self.plr.messages)
        self.assertIn('| Played: Moat', self.plr.messages)

    def test_reserve(self):
        self.plr.messages = []
        self.plr.setReserve('Copper')
        self.plr.displayOverview()
        self.assertIn('| Reserve: Copper', self.plr.messages)

    def test_duration(self):
        self.plr.messages = []
        self.plr.durationpile.add(self.g['Copper'].remove())
        self.plr.displayOverview()
        self.assertIn('| Duration: Copper', self.plr.messages)

    def test_discards(self):
        self.plr.messages = []
        self.plr.setDiscard('Copper')
        self.plr.displayOverview()
        self.assertIn('| 1 cards in discard pile', self.plr.messages)

    def test_project(self):
        self.plr.messages = []
        self.plr.assign_project('Cathedral')
        self.plr.displayOverview()
        self.assertIn('| Project: Cathedral', self.plr.messages)

    def test_artifact(self):
        self.plr.messages = []
        self.plr.assign_artifact('Horn')
        self.plr.displayOverview()
        self.assertIn('| Artifacts: Horn', self.plr.messages)


###############################################################################
class Test_buyable_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'], badcards=['Coppersmith'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g['Moat'].remove()

    def test_buy_moat(self):
        self.plr.addCoin(3)
        opts, ind = self.plr.buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i['name'] == 'Moat':
                self.assertEqual(i['verb'], 'Buy')
                self.assertEqual(i['action'], 'buy')
                self.assertEqual(i['card'], self.g['Moat'])
                break
        else:   # pragma: no coverage
            self.fail("Moat not buyable")

    def test_buy_copper(self):
        self.plr.coin = 0
        opts, ind = self.plr.buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i['name'].startswith('Copper'):
                try:
                    self.assertEqual(i['action'], 'buy')
                    self.assertEqual(i['card'], self.g['Copper'])
                except AssertionError:      # pragma: no cover
                    print("Buy Copper {}".format(i))
                    self.g.print_state()
                    raise
                break
        else:   # pragma: no coverage
            self.fail("Copper not buyable")

    def test_buy_token(self):
        self.plr.addCoin(2)
        self.plr.place_token('+1 Card', 'Moat')
        opts, ind = self.plr.buyable_selection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i['name'] == 'Moat':
                self.assertIn('[Tkn: +1 Card]', i['details'])
                break
        else:   # pragma: no coverage
            self.fail("Moat not buyable")


###############################################################################
class Test_playable_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g['Moat'].remove()

    def test_play(self):
        self.plr.addCard(self.moat, 'hand')
        opts, ind = self.plr.playable_selection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]['selector'], 'b')
        self.assertEqual(opts[0]['card'], self.moat)
        self.assertEqual(opts[0]['desc'], '+2 cards, defense')
        self.assertEqual(opts[0]['verb'], 'Play')
        self.assertEqual(opts[0]['name'], 'Moat')
        self.assertEqual(ind, 2)

    def test_token(self):
        self.plr.place_token('+1 Card', 'Moat')
        self.plr.addCard(self.moat, 'hand')
        opts, ind = self.plr.playable_selection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]['selector'], 'b')
        self.assertEqual(opts[0]['card'], self.moat)
        self.assertTrue('[Tkn: +1 Card]' in opts[0]['notes'])
        self.assertEqual(ind, 2)


###############################################################################
class Test_choice_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat', 'Alchemist'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g['Moat'].remove()
        self.potion = self.g['Potion'].remove()

    def test_action_phase(self):
        self.plr.setHand('Moat')
        self.plr.phase = 'action'
        opts, _ = self.plr.choice_selection()

        self.assertEqual(opts[0]['verb'], 'End Phase')
        self.assertEqual(opts[0]['action'], 'quit')
        self.assertEqual(opts[0]['selector'], '0')
        self.assertIsNone(opts[0]['card'])

        self.assertEqual(opts[1]['verb'], 'Play')
        self.assertEqual(opts[1]['name'], 'Moat')
        self.assertEqual(opts[1]['action'], 'play')
        self.assertEqual(opts[1]['selector'], 'a')

        self.assertEqual(len(opts), 2)

    def test_buy_phase(self):
        self.plr.setHand('Copper')
        self.plr.phase = 'buy'
        self.plr.coffer = 0   # Stop card choice_selection breaking test
        opts, _ = self.plr.choice_selection()

        self.assertEqual(opts[0]['verb'], 'End Phase')
        self.assertEqual(opts[0]['action'], 'quit')
        self.assertEqual(opts[0]['selector'], '0')
        self.assertIsNone(opts[0]['card'])

        self.assertEqual(opts[1]['action'], 'spendall')
        self.assertEqual(opts[2]['action'], 'spend')

    def test_prompt(self):
        self.plr.actions = 3
        self.plr.buys = 7
        self.plr.potions = 9
        self.plr.coin = 5
        self.plr.coffer = 1
        self.plr.phase = 'buy'
        self.plr.debt = 2
        _, prompt = self.plr.choice_selection()
        self.assertIn('Actions=3', prompt)
        self.assertIn('Coins=5', prompt)
        self.assertIn('Buys=7', prompt)
        self.assertIn('Debt=2', prompt)
        self.assertIn('Potion', prompt)
        self.assertIn('Coffer=1', prompt)

    def test_nothing_prompt(self):
        self.plr.actions = 0
        self.plr.buys = 0
        self.plr.potions = 0
        self.plr.coin = 0
        self.plr.coffer = 0
        self.plr.phase = 'buy'
        _, prompt = self.plr.choice_selection()
        self.assertIn('Actions=0', prompt)
        self.assertIn('Buys=0', prompt)
        self.assertNotIn('Coins', prompt)
        self.assertNotIn('Potions', prompt)
        self.assertNotIn('Coffer', prompt)


###############################################################################
class Test_night_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Monastery', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g['Moat'].remove()

    def test_play(self):
        self.plr.setHand('Copper', 'Moat', 'Monastery')
        opts, idx = self.plr.night_selection(1)
        self.assertEqual(idx, 2)
        self.assertEqual(opts[0]['selector'], 'b')
        self.assertEqual(opts[0]['verb'], 'Play')
        self.assertEqual(opts[0]['action'], 'play')
        self.assertEqual(opts[0]['card'].name, 'Monastery')

    def test_no_night(self):
        self.plr.setHand('Copper', 'Moat')
        opts = self.plr.night_selection(0)
        self.assertEqual(opts, ([], 0))


###############################################################################
class Test_spendable_selection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat', 'Alchemist'], badcards=['Baker'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.moat = self.g['Moat'].remove()
        self.potion = self.g['Potion'].remove()

    def test_play(self):
        self.plr.setHand('Copper', 'Estate')
        self.plr.addCard(self.potion, 'hand')
        self.plr.addCard(self.moat, 'hand')
        self.plr.gainCoffer(1)
        self.plr.gainVillager(1)
        opts = self.plr.spendable_selection()
        self.assertEqual(opts[0]['selector'], '1')
        self.assertEqual(opts[0]['action'], 'spendall')
        self.assertIn('Spend all treasures', opts[0]['verb'])
        self.assertIsNone(opts[0]['card'])

        self.assertEqual(opts[1]['selector'], '2')
        self.assertEqual(opts[1]['verb'], 'Spend Coffer (1 coin)')
        self.assertEqual(opts[1]['action'], 'coffer')
        self.assertIsNone(opts[1]['card'])

        self.assertEqual(opts[2]['selector'], '4')
        self.assertEqual(opts[2]['verb'], 'Spend')
        self.assertEqual(opts[2]['name'], 'Copper')
        self.assertEqual(opts[2]['action'], 'spend')
        self.assertEqual(opts[2]['card'].name, 'Copper')

        self.assertEqual(opts[3]['verb'], 'Spend')
        self.assertEqual(opts[3]['selector'], '5')
        self.assertEqual(opts[3]['action'], 'spend')
        self.assertEqual(opts[3]['card'].name, 'Potion')

    def test_debt(self):
        self.plr.setHand('Copper')
        self.plr.debt = 1
        self.plr.coin = 1
        self.plr.coffer = 0
        try:
            opts = self.plr.spendable_selection()
            self.assertEqual(opts[1]['selector'], '3')
            self.assertEqual(opts[1]['action'], 'payback')
            self.assertEqual(opts[1]['verb'], 'Payback Debt')
            self.assertIsNone(opts[1]['card'])
        except AssertionError:      # pragma: no cover
            print("debt")
            self.g.print_state()
            raise


###############################################################################
class Test_buyCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Embargo'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_debt(self):
        self.plr.debt = 1
        self.plr.buyCard(self.g['Copper'])
        self.assertIn('Must pay off debt first', self.plr.messages)

    def test_embargo(self):
        self.g['Copper'].embargo()
        self.plr.buyCard(self.g['Copper'])
        self.assertIsNotNone(self.plr.inDiscard('Curse'))
        self.assertIn('Gained a Curse from embargo', self.plr.messages)


###############################################################################
class Test_spendCoffer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_spendCoffer(self):
        """ Spend a coffer that the player has """
        self.plr.coffer = 1
        self.plr.spendCoffer()
        self.assertEqual(self.plr.getCoffer(), 0)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_spendNothing(self):
        """ Spend a coffer that the player doesn't have """
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
        """ Spend a Villager that the player has """
        self.plr.villager = 1
        self.plr.spendVillager()
        self.assertEqual(self.plr.getVillager(), 0)
        self.assertEqual(self.plr.getActions(), 2)

    def test_spendNothing(self):
        """ Spend a Villager that the player doesn't have """
        self.plr.villager = 0
        self.plr.spendVillager()
        self.assertEqual(self.plr.getVillager(), 0)
        self.assertEqual(self.plr.getActions(), 1)


###############################################################################
class Test_plrGainCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_gainCard_equal(self):
        self.plr.test_input = ['get silver']
        c = self.plr.plrGainCard(3, modifier='equal')
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertEqual(c.name, 'Silver')

    def test_gainCard_less(self):
        self.plr.test_input = ['get silver']
        c = self.plr.plrGainCard(4, modifier='less')
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertEqual(c.name, 'Silver')


###############################################################################
class Test_exile(unittest.TestCase):
    """ Test exile pile """
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_in_exile(self):
        self.plr.set_exile('Silver')
        self.assertIsNotNone(self.plr.in_exile('Silver'))

    def test_exile_card(self):
        au_card = self.g['Gold'].remove()
        self.plr.set_exile()
        self.plr.exile_card(au_card)
        self.assertIsNotNone(self.plr.in_exile('Gold'))


###############################################################################
class Test_plrDiscardDownTo(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_discard_nothing(self):
        self.plr.setHand('Estate', 'Duchy', 'Province')
        self.plr.plrDiscardDownTo(3)
        self.assertEqual(self.plr.discardSize(), 0)

    def test_discard_one(self):
        self.plr.test_input = ['gold', 'finish']
        self.plr.setHand('Estate', 'Duchy', 'Province', 'Gold')
        self.plr.plrDiscardDownTo(3)
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
