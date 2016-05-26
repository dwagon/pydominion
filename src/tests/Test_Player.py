#!/usr/bin/env python

import unittest
import Game


###############################################################################
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_initialCardStacks(self):
        """ Make sure initial hands are correct """
        self.assertEqual(len(self.plr.deck), 5)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.playedSize(), 0)
        self.assertEqual(self.plr.discardSize(), 0)

    def test_initialDeck(self):
        """ Ensure initial player decks are correct """
        self.plr.deck.empty()
        self.plr.initial_Deck()
        self.assertEqual(len(self.plr.deck), 10)

    def test_trashcard(self):
        """ Test that trashing a card works """
        numcards = self.g.countCards()
        card = self.plr.hand[0]
        self.plr.trashCard(card)
        self.assertEqual(numcards, self.g.countCards())
        self.assertEqual(self.g.trashpile[0], card)

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_discard(self):
        self.plr.setHand('Copper', 'Silver')
        self.plr.setPlayed('Estate', 'Duchy')
        self.plr.discardHand()
        self.assertEqual(self.plr.handSize(), 0)
        self.assertEqual(self.plr.playedSize(), 0)
        self.assertEqual(self.plr.discardSize(), 4)


###############################################################################
class Test_inDiscard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_once(self):
        x = self.plr.do_once('test')
        self.assertTrue(x)
        x = self.plr.do_once('test')
        self.assertFalse(x)


###############################################################################
class Test_cardsAffordable(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_under(self):
        price = 4
        ans = self.plr.cardsUnder(price, types={'action': True})
        for a in ans:
            self.assertLessEqual(a.cost, price)
            self.assertTrue(a.isAction())

    def test_worth(self):
        price = 5
        ans = self.plr.cardsWorth(price, types={'victory': True})
        for a in ans:
            self.assertEqual(a.cost, price)
            self.assertTrue(a.isVictory())


###############################################################################
class Test_typeSelector(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_None(self):
        self.plr.setHand('Gold')
        self.plr.test_input = ['0']
        x = self.plr.plrTrashCard()
        self.assertEqual(x, [])
        self.assertTrue(self.g.trashpile.isEmpty())

    def test_Two(self):
        self.plr.setHand('Gold', 'Copper', 'Silver')
        self.plr.test_input = ['1', '2', '0']
        x = self.plr.plrTrashCard(num=2)
        self.assertEqual(len(x), 2)
        self.assertEqual(self.g.trashpile.cards, x)

    def test_Trash(self):
        self.plr.setHand('Gold')
        self.plr.test_input = ['1']
        x = self.plr.plrTrashCard()
        self.assertEqual(x[0].name, 'Gold')
        self.assertEqual(len(self.g.trashpile), 1)
        self.assertEqual(self.g.trashpile[-1].name, 'Gold')

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.g.startGame()
        self.plr, self.defend, self.victim = self.g.playerList()
        self.defend.setHand('Moat')

    def test_output(self):
        v = self.plr.attackVictims()
        self.assertEqual(v, [self.victim])


###############################################################################
class Test_inDeck(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_indeck(self):
        """ Test card is in deck """
        self.plr.setDeck('Copper')
        self.assertTrue(self.plr.inDeck('Copper'))
        self.assertEqual(self.plr.inDeck('Copper').name, 'Copper')

    def test_notindeck(self):
        """ Test card that isn't in deck """
        self.plr.setDeck('Copper')
        self.assertFalse(self.plr.inDeck('Estate'))


###############################################################################
class Test_inHand(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
            if msg.startswith('test'):
                count += 1
        self.assertEqual(count, 3)


###############################################################################
class Test_misc(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Golem', 'Witch'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

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
        self.assertEqual(self.plr.coststr(witch), "3 coins")
        self.assertEqual(self.plr.coststr(golem), "4 coins 1 potions")

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
        self.plr.cleanupPhase()
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.playedSize(), 0)


###############################################################################
class Test_displayOverview(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_empty(self):
        self.plr.messages = []
        self.plr.setHand()
        self.plr.setPlayed()
        self.plr.displayOverview()
        self.assertIn('| Hand: <EMPTY>', self.plr.messages)
        self.assertIn('| Played: <NONE>', self.plr.messages)
        self.assertEquals(len(self.plr.messages), 5)

    def test_non_empty(self):
        self.plr.messages = []
        self.plr.setHand('Copper', 'Estate')
        self.plr.setPlayed('Moat')
        self.plr.displayOverview()
        self.assertIn('| Hand: Copper, Estate', self.plr.messages)
        self.assertIn('| Played: Moat', self.plr.messages)
        self.assertEquals(len(self.plr.messages), 5)

    def test_reserve(self):
        self.plr.messages = []
        self.plr.setReserve('Copper')
        self.plr.displayOverview()
        self.assertIn('| Reserve: Copper', self.plr.messages)
        self.assertEquals(len(self.plr.messages), 6)

    def test_duration(self):
        self.plr.messages = []
        self.plr.durationpile.add(self.g['Copper'].remove())
        self.plr.displayOverview()
        self.assertIn('| Duration: Copper', self.plr.messages)


###############################################################################
class Test_buyableSelection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.moat = self.g['Moat'].remove()

    def test_buy_moat(self):
        self.plr.addCoin(3)
        opts, ind = self.plr.buyableSelection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i['print'].startswith('Buy Moat'):
                self.assertEqual(i['action'], 'buy')
                self.assertEqual(i['card'], self.g['Moat'])
                break
        else:   # pragma: no coverage
            self.fail("Moat not buyable")

    def test_buy_copper(self):
        self.plr.coin = 0
        opts, ind = self.plr.buyableSelection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i['print'].startswith('Buy Copper'):
                self.assertEqual(i['action'], 'buy')
                self.assertEqual(i['card'], self.g['Copper'])
                break
        else:   # pragma: no coverage
            self.fail("Copper not buyable")

    def test_buy_token(self):
        self.plr.addCoin(2)
        self.plr.place_token('+1 Card', 'Moat')
        opts, ind = self.plr.buyableSelection(1)
        self.assertEqual(ind, 1 + len(opts))
        for i in opts:
            if i['print'].startswith('Buy Moat'):
                self.assertIn('[Tkn: +1 Card]', i['print'])
                break
        else:   # pragma: no coverage
            self.fail("Moat not buyable")


###############################################################################
class Test_playableSelection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.moat = self.g['Moat'].remove()

    def test_play(self):
        self.plr.addCard(self.moat, 'hand')
        opts, ind = self.plr.playableSelection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]['selector'], 'b')
        self.assertEqual(opts[0]['card'], self.moat)
        self.assertEqual(opts[0]['print'], 'Play Moat (+2 cards, defense)')
        self.assertEqual(ind, 2)

    def test_token(self):
        self.plr.place_token('+1 Card', 'Moat')
        self.plr.addCard(self.moat, 'hand')
        opts, ind = self.plr.playableSelection(1)
        self.assertEqual(len(opts), 1)
        self.assertEqual(opts[0]['selector'], 'b')
        self.assertEqual(opts[0]['card'], self.moat)
        self.assertTrue('[Tkn: +1 Card]' in opts[0]['print'])
        self.assertEqual(ind, 2)


###############################################################################
class Test_choiceSelection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat', 'Alchemist'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.moat = self.g['Moat'].remove()
        self.potion = self.g['Potion'].remove()

    def test_action_phase(self):
        self.plr.setHand('Moat')
        opts, prompt = self.plr.choiceSelection('action')

        self.assertEqual(opts[0]['print'], 'End Phase')
        self.assertEqual(opts[0]['action'], 'quit')
        self.assertEqual(opts[0]['selector'], '0')
        self.assertIsNone(opts[0]['card'])

        self.assertTrue(opts[1]['print'].startswith('Play Moat'))
        self.assertEqual(opts[1]['action'], 'play')
        self.assertEqual(opts[1]['selector'], 'a')

        self.assertEqual(len(opts), 2)

    def test_buy_phase(self):
        self.plr.setHand('Copper')
        opts, prompt = self.plr.choiceSelection('buy')

        self.assertEqual(opts[0]['print'], 'End Phase')
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
        self.plr.specialcoins = 1
        opts, prompt = self.plr.choiceSelection('buy')
        self.assertIn('Actions=3', prompt)
        self.assertIn('Coins=5', prompt)
        self.assertIn('Buys=7', prompt)
        self.assertIn('Potions=9', prompt)
        self.assertIn('Special Coins=1', prompt)

    def test_nothing_prompt(self):
        self.plr.actions = 0
        self.plr.buys = 0
        self.plr.potions = 0
        self.plr.coin = 0
        self.plr.specialcoins = 0
        opts, prompt = self.plr.choiceSelection('buy')
        self.assertIn('Actions=0', prompt)
        self.assertIn('Buys=0', prompt)
        self.assertNotIn('Coins', prompt)
        self.assertNotIn('Potions', prompt)
        self.assertNotIn('Special Coins', prompt)


###############################################################################
class Test_spendableSelection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat', 'Alchemist'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.moat = self.g['Moat'].remove()
        self.potion = self.g['Potion'].remove()

    def test_play(self):
        self.plr.setHand('Copper', 'Estate')
        self.plr.addCard(self.potion, 'hand')
        self.plr.addCard(self.moat, 'hand')
        self.plr.gainSpecialCoins(1)
        opts = self.plr.spendableSelection()
        self.assertEqual(opts[0]['selector'], '1')
        self.assertEqual(opts[0]['action'], 'spendall')
        self.assertTrue(opts[0]['print'].startswith('Spend all treasures'))
        self.assertIsNone(opts[0]['card'])

        self.assertEqual(opts[1]['selector'], '2')
        self.assertEqual(opts[1]['print'], 'Spend Coin')
        self.assertEqual(opts[1]['action'], 'coin')
        self.assertIsNone(opts[1]['card'])

        self.assertTrue(opts[2]['print'].startswith('Spend Copper'))
        self.assertEqual(opts[2]['selector'], '3')
        self.assertEqual(opts[2]['action'], 'spend')
        self.assertEqual(opts[2]['card'].name, 'Copper')

        self.assertTrue(opts[3]['print'].startswith('Spend Potion'))
        self.assertEqual(opts[3]['selector'], '4')
        self.assertEqual(opts[3]['action'], 'spend')
        self.assertEqual(opts[3]['card'].name, 'Potion')


###############################################################################
class Test_spendCoin(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_spendCoin(self):
        """ Spend a coin that the player has """
        self.plr.specialcoins = 1
        self.plr.spendCoin()
        self.assertEqual(self.plr.getSpecialCoins(), 0)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_spendNothing(self):
        """ Spend a coin that the player doesn't have """
        self.plr.specialcoins = 0
        self.plr.spendCoin()
        self.assertEqual(self.plr.getSpecialCoins(), 0)
        self.assertEqual(self.plr.getCoin(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
