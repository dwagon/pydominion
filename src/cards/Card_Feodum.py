#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Feodum(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.VICTORY
        self.base = Game.DARKAGES
        self.desc = "1VP / 3 silvers - trash for 3 silvers"
        self.name = 'Feodum'
        self.playable = False
        self.cost = 4

    def special_score(self, game, player):
        """ Worth 1VP for every 3 silvers cards in your deck rounded down """
        numsilver = 0
        for c in player.allCards():
            if c.name == 'Silver':
                numsilver += 1
        return int(numsilver / 3)

    def hook_trashThisCard(self, game, player):
        """ When you trash this gain 3 silvers """
        for _ in range(3):
            player.gainCard('Silver')


###############################################################################
class Test_Feodum(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Feodum'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_scoreOne(self):
        self.plr.setHand('Feodum')
        self.plr.setDeck('Copper')
        self.plr.setDiscard('Silver', 'Silver', 'Silver', 'Silver')
        self.assertEqual(self.plr.getScoreDetails()['Feodum'], 1)

    def test_scoreTwo(self):
        self.plr.setHand('Feodum')
        self.plr.setDeck('Feodum')
        self.plr.setDiscard('Silver', 'Silver', 'Silver', 'Silver', 'Silver', 'Silver')
        self.assertEqual(self.plr.getScoreDetails()['Feodum'], 4)

    def test_trash(self):
        """ Trash a Feodum card """
        card = self.g['Feodum'].remove()
        self.plr.addCard(card, 'hand')
        self.plr.trashCard(card)
        self.assertEqual(self.plr.discard_size(), 3)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Silver')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
