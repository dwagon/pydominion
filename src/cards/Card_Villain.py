#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Villain(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'renaissance'
        self.name = 'Villain'
        self.desc = "+2 Coffers; Each other player with 5 or more cards in hand discards one costing 2 or more (or reveals they can't)."
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        player.gainCoffer(2)
        for vic in player.attackVictims():
            if vic.handSize() >= 5:
                from_cards = []
                for card in vic.hand:
                    if card.cost >= 2:
                        from_cards.append(card)
                if from_cards:
                    disc = vic.plrDiscardCards(
                        prompt="{}'s Villain forcing you to discard one card".format(player.name),
                        cardsrc=from_cards, num=1
                        )
                    player.output("{} discarded {}".format(vic.name, disc[0].name))
                else:
                    player.output("{} had no appropriate cards".format(vic.name))
            else:
                player.output("{}'s hand size is too small".format(vic.name))


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):  # oragma: no cover
    # Discard a victory card first, then whichever
    for card in kwargs['cardsrc']:
        if card.isVictory():
            return [card]
    return [kwargs['cardsrc'][0]]


###############################################################################
class Test_Villain(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Villain'], numhexes=0, numboons=0)
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Villain'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playCard(self):
        self.vic.setHand('Gold', 'Province', 'Copper', 'Copper', 'Copper')
        self.vic.test_input = ['Province']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoffer(), 2)
        self.assertIsNotNone(self.vic.inDiscard('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
