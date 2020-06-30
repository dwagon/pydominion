#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Sacrifice(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.desc = """Trash a card from your hand. If it's an ...
        Action card: +2 Cards, +2 Actions;
        Treasure card: +2 Coin;
        Victory card: +2VP"""
        self.name = 'Sacrifice'
        self.cost = 4

    def special(self, game, player):
        cards = player.plrTrashCard()
        if not cards:
            return
        card = cards[0]
        if card.isAction():
            player.pickupCards(2)
            player.addActions(2)
        if card.isTreasure():
            player.addCoin(2)
        if card.isVictory():
            player.addScore('Sacrifice', 2)


###############################################################################
class Test_Sacrifice(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Sacrifice', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Sacrifice'].remove()

    def test_play_action(self):
        """ Sacrifice an Action """
        self.plr.setHand('Moat')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['moat']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertIsNotNone(self.g.in_trash('Moat'))

    def test_play_treasure(self):
        """ Sacrifice a Treasure """
        self.plr.setHand('Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['silver']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_play_victory(self):
        """ Sacrifice a Victory """
        self.plr.setHand('Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['duchy']
        self.plr.playCard(self.card)
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Sacrifice'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
