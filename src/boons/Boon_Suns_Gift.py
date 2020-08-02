#!/usr/bin/env python

import unittest
import Game
from Boon import Boon


###############################################################################
class Boon_Suns_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocturne'
        self.desc = "Look at the top 4 cards of your deck. Discard any number of them and put the rest back in any order."
        self.name = "The Sun's Gift"
        self.purchasable = False

    def special(self, game, player):
        cards = []
        for _ in range(4):
            c = player.nextCard()
            if c:
                cards.append(c)
        todisc = player.plrDiscardCards(prompt="Discard any number and the rest go back on the top of the deck", anynum=True, cardsrc=cards)
        for card in cards:
            if card not in todisc:
                player.addCard(card, 'topdeck')


###############################################################################
class Test_Suns_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Sun's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_suns_gift(self):
        self.plr.setDeck('Silver', 'Gold', 'Province', 'Duchy', 'Copper')
        self.plr.test_input = ['Province', 'Duchy', 'finish']
        self.plr.playCard(self.card)
        try:
            self.assertIsNotNone(self.plr.in_deck('Silver'))
            self.assertIsNotNone(self.plr.in_deck('Gold'))
            self.assertIsNotNone(self.plr.inDiscard('Province'))
            self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
