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
        estate = self.g['estate'].remove()
        gold = self.g['gold'].remove()
        self.plr.addCard(estate, 'deck')
        self.plr.addCard(gold, 'topdeck')
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Gold')


###############################################################################
class Test_nextCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_emptyDeck(self):
        self.plr.deck.empty()
        self.plr.setDiscard('gold')
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Gold')

    def test_noCards(self):
        self.plr.deck.empty()
        self.plr.discardpile.empty()
        c = self.plr.nextCard()
        self.assertEqual(c, None)

    def test_drawOne(self):
        self.plr.setDeck('province')
        self.plr.discardpile.empty()
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Province')
        self.assertTrue(self.plr.deck.isEmpty())


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
        self.plr.setHand('gold')
        self.plr.test_input = ['0']
        x = self.plr.plrTrashCard()
        self.assertEqual(x, [])
        self.assertTrue(self.g.trashpile.isEmpty())

    def test_Two(self):
        self.plr.setHand('gold', 'copper', 'silver')
        self.plr.test_input = ['1', '2', '0']
        x = self.plr.plrTrashCard(num=2)
        self.assertEqual(len(x), 2)
        self.assertEqual(self.g.trashpile.cards, x)

    def test_Trash(self):
        self.plr.setHand('gold')
        self.plr.test_input = ['1']
        x = self.plr.plrTrashCard()
        self.assertEqual(x[0].name, 'Gold')
        self.assertEqual(len(self.g.trashpile), 1)
        self.assertEqual(self.g.trashpile[-1].name, 'Gold')

    def test_Force(self):
        self.plr.setHand('gold')
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
        self.plr.setHand('gold', 'gold', 'copper')
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
        self.plr.setHand('copper', 'estate', 'province', 'gold')
        self.plr.test_input = ['0']
        x = self.plr.plrDiscardCards(0)
        self.assertEqual(x, [])
        self.assertEqual(len(self.plr.hand), 4)
        self.assertTrue(self.plr.discardpile.isEmpty())

    def test_discardOne(self):
        self.plr.setHand('copper', 'estate', 'province', 'gold')
        self.plr.test_input = ['1', '0']
        x = self.plr.plrDiscardCards(1)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile.cards)

    def test_discardAnynum(self):
        self.plr.setHand('copper', 'estate', 'province', 'gold')
        self.plr.test_input = ['1', '0']
        x = self.plr.plrDiscardCards(0, anynum=True)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile)


###############################################################################
class Test_attackVictims(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=3, initcards=['moat'])
        self.g.startGame()
        self.plr, self.defend, self.victim = self.g.playerList()
        self.defend.setHand('moat')

    def test_output(self):
        v = self.plr.attackVictims()
        self.assertEqual(v, [self.victim])


###############################################################################
class Test_inHand(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_inhand(self):
        """ Test card is in hand """
        self.plr.setHand('copper')
        self.assertTrue(self.plr.inHand('Copper'))

    def test_notinhand(self):
        """ Test card that isn't in hand """
        self.plr.setHand('copper')
        self.assertFalse(self.plr.inHand('Estate'))


###############################################################################
class Test_gainCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_gainByString(self):
        self.plr.gainCard('copper')
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')

    def test_gainByCardpile(self):
        cp = self.g['copper']
        self.plr.gainCard(cp)
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')

    def test_gainSpecific(self):
        cu = self.g['copper'].remove()
        self.plr.gainCard(newcard=cu)
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')

    def test_destination(self):
        self.plr.hand.empty()
        self.plr.gainCard('copper', 'hand')
        self.assertTrue(self.plr.discardpile.isEmpty())
        self.assertEqual(self.plr.hand[0].name, 'Copper')


###############################################################################
class Test_spendAllCards(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_spendCards(self):
        """ Spend all cards in hand"""
        self.plr.setHand('gold', 'silver', 'estate', 'moat')
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
        self.plr.setDeck('gold')
        self.plr.setHand()
        self.plr.pickupCard()
        self.assertEqual(self.plr.hand[0].name, 'Gold')
        self.assertEqual(self.plr.deckSize(), 0)
        self.assertEqual(self.plr.handSize(), 1)

    def test_pickup_empty(self):
        """ Test picking up a card from an empty deck"""
        self.plr.setDeck()
        self.plr.setDiscard('gold')
        self.plr.setHand()
        self.plr.pickupCard()
        self.assertEqual(self.plr.hand[0].name, 'Gold')
        self.assertEqual(self.plr.deckSize(), 0)
        self.assertEqual(self.plr.handSize(), 1)


###############################################################################
class Test_args(unittest.TestCase):
    def setUp(self):
        pass

    def test_numplayers(self):
        g = Game.Game(quiet=True, numplayers=4)
        g.startGame()
        self.assertEqual(len(g.playerList()), 4)

    def test_card(self):
        g = Game.Game(quiet=True, initcards=['moat'])
        g.startGame()
        self.assertTrue('Moat' in g.cardpiles)

    def test_prosperity(self):
        g = Game.Game(quiet=True, prosperity=True)
        g.startGame()
        self.assertTrue('Colony' in g.cardpiles)
        self.assertTrue('Platinum' in g.cardpiles)


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
class test_game_over(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_not_over(self):
        """ The game isn't over yet """
        over = self.g.isGameOver()
        self.assertFalse(over)

    def test_provinces(self):
        """ Someone took the last province """
        for i in range(200):
            self.plr.gainCard('province')
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_three_stacks(self):
        """ Three stacks are empty """
        for i in range(200):
            self.plr.gainCard('estate')
            self.plr.gainCard('copper')
            self.plr.gainCard('silver')
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_two_stacks(self):
        """ Two stacks are empty """
        for i in range(200):
            self.plr.gainCard('estate')
            self.plr.gainCard('silver')
        over = self.g.isGameOver()
        self.assertFalse(over)


###############################################################################
class Test_whowon(unittest.TestCase):
    def setUp(self):
        self.numplayers = 3
        self.g = Game.Game(quiet=True, numplayers=self.numplayers)
        self.g.startGame()

    def test_whoWon(self):
        scores = self.g.whoWon()
        # Everyone should get 3 estates at start
        for score in scores.values():
            self.assertEqual(score, 3)
        self.assertEqual(len(scores), self.numplayers)


###############################################################################
class Test_parse_args(unittest.TestCase):
    def test_defaults(self):
        args = Game.parseArgs([])
        self.assertEqual(args.numplayers, 2)
        self.assertEqual(args.cardbase, None)
        self.assertEqual(args.prosperity, False)
        self.assertEqual(args.initcards, [])

    def test_prosperity(self):
        args = Game.parseArgs(['--prosperity'])
        self.assertEqual(args.prosperity, True)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
