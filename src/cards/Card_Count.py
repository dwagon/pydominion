#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Count(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "Lots of choices"
        self.name = 'Count'
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        """ Choose one: Discard 2 cards; or put a card from your
        hand on top of your deck; or gain a copper.

        Choose one: +3 coin, or trash your hand or gain a Duchy """

        ans = player.plrChooseOptions(
            "What do you want to do?",
            ("Discard 2 cards", "discard"),
            ("Put a card from you hand on top of your deck", "putcard"),
            ("Gain a copper", "copper")
        )
        if ans == 'copper':
            player.output("Gained a copper")
            player.gainCard('copper')
        elif ans == 'putcard':
            self.putCard(game, player)
        else:
            player.plrDiscardCards(2)

        ans = player.plrChooseOptions(
            'What do you want to do now?',
            ('+3 coin', 'coin'), ('Trash hand', 'trash'), ('Gain Duchy', 'duchy'))
        if ans == 'duchy':
            player.output("Gained a duchy")
            player.gainCard('duchy')
        elif ans == 'trash':
            for c in player.hand[:]:
                player.output("Trashing %s" % c.name)
                player.trashCard(c)
        else:
            player.addCoin(3)

    ###########################################################################
    def putCard(self, game, player):
        """ Put a card from your hand on top of your deck """
        index = 1
        options = []
        for c in player.hand:
            sel = '%d' % index
            pr = 'Put %s on top of your deck' % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Select card to put on top of your deck")
        player.output("Moving %s to top of deck" % o['card'].name)
        player.addCard(o['card'], 'topdeck')
        player.hand.remove(o['card'])


###############################################################################
class Test_Count(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['count'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['count'].remove()
        self.plr.setHand('copper', 'estate', 'silver', 'province', 'gold')

    def test_discard(self):
        self.plr.addCard(self.card, 'hand')
        # Discard, select card 1 and card 2, finish selecting, +3 gold
        self.plr.test_input = ['discard 2', 'discard estate', 'discard copper', 'finish', '+3 gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardSize(), 2)
        self.assertEqual(self.plr.handSize(), 3)

    def test_topdeck(self):
        self.plr.setHand('gold')
        self.plr.addCard(self.card, 'hand')
        # top deck, card select, +3 gold
        self.plr.test_input = ['top of your deck', 'put gold', '+3 gold']
        self.plr.playCard(self.card)
        nc = self.plr.nextCard()
        self.assertEqual(nc.name, 'Gold')

    def test_gainCopper(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['gain a copper', '+3 gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')

    def test_gaingold(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['gain a copper', '+3 gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)

    def test_trashhand(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['gain a copper', 'trash hand']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand, [])
        self.assertEqual(self.g.trashSize(), 5)

    def test_gainDuchy(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['gain a copper', 'gain duchy']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[1].name, 'Duchy')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
