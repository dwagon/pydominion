#!/usr/bin/env python

import unittest
import Game


###############################################################################
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

    def test_initialCardStacks(self):
        """ Make sure initial hands are correct """
        self.assertEqual(len(self.plr.deck), 5)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.played, [])
        self.assertEqual(self.plr.discardpile, [])

    def test_initialDeck(self):
        """ Ensure initial player decks are correct """
        self.plr.deck = []
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
        self.plr.deck = []
        estate = self.g['estate'].remove()
        gold = self.g['gold'].remove()
        self.plr.addCard(estate, 'deck')
        self.plr.addCard(gold, 'topdeck')
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Gold')


###############################################################################
class Test_nextCard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

    def test_emptyDeck(self):
        self.plr.deck = []
        self.plr.setDiscard('gold')
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Gold')

    def test_noCards(self):
        self.plr.deck = []
        self.plr.discardpile = []
        c = self.plr.nextCard()
        self.assertEqual(c, None)

    def test_drawOne(self):
        self.plr.setDeck('province')
        self.plr.discardpile = []
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Province')
        self.assertEqual(self.plr.deck, [])


###############################################################################
class Test_cardsAffordable(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

    def test_None(self):
        self.plr.setHand('gold')
        self.plr.test_input = ['0']
        x = self.plr.plrTrashCard()
        self.assertEqual(x, [])
        self.assertEqual(self.g.trashpile, [])

    def test_Two(self):
        self.plr.setHand('gold', 'copper', 'silver')
        self.plr.test_input = ['1', '2', '0']
        x = self.plr.plrTrashCard(num=2)
        self.assertEqual(len(x), 2)
        self.assertEqual(self.g.trashpile, x)

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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

    def test_discardNone(self):
        self.plr.setHand('copper', 'estate', 'province', 'gold')
        self.plr.test_input = ['0']
        x = self.plr.plrDiscardCards(0)
        self.assertEqual(x, [])
        self.assertEqual(len(self.plr.hand), 4)
        self.assertEqual(self.plr.discardpile, [])

    def test_discardOne(self):
        self.plr.setHand('copper', 'estate', 'province', 'gold')
        self.plr.test_input = ['1', '0']
        x = self.plr.plrDiscardCards(1)
        self.assertEqual(len(x), 1)
        self.assertEqual(len(self.plr.hand), 3)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(x, self.plr.discardpile)

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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=3, initcards=['moat'])
        self.plr = self.g.players[0]
        self.defend = self.g.players[1]
        self.victim = self.g.players[2]
        self.defend.setHand('moat')

    def test_output(self):
        v = self.plr.attackVictims()
        self.assertEqual(v, [self.victim])


###############################################################################
class Test_inHand(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

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
        self.plr.hand = []
        self.plr.gainCard('copper', 'hand')
        self.assertEqual(self.plr.discardpile, [])
        self.assertEqual(self.plr.hand[0].name, 'Copper')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
