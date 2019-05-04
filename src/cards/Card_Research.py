#!/usr/bin/env python

import unittest
from Card import Card
from PlayArea import PlayArea


###############################################################################
class Card_Research(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'renaissance'
        self.name = 'Research'
        self.desc = """+1 Action; Trash a card from your hand.
            Per coin it costs, set aside a card from your deck face down.
            At the start of your next turn, put those cards into your hand."""
        self.cost = 4
        self.actions = 1

    ###########################################################################
    def special(self, game, player):
        if not hasattr(player, '_research'):
            player._research = PlayArea([])
        tc = player.plrTrashCard(num=1, force=True, printcost=True)
        cost = tc[0].cost
        if cost == 0:
            return
        cards = player.cardSel(
            prompt='Set aside {} cards for next turn'.format(cost),
            verbs=('Set', 'Unset'),
            num=cost,
            cardsrc='hand'
            )
        for card in cards:
            player._research.add(card)
            player.hand.remove(card)
            player.secret_count += 1

    ###########################################################################
    def duration(self, game, player):
        cards = []
        for card in player._research:
            cards.append(card)
        for card in cards:
            player.output("Bringing {} out from research".format(card.name))
            player.addCard(card, 'hand')
            player._research.remove(card)
            player.secret_count -= 1


###############################################################################
class Test_Research(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Research', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Research'].remove()
        self.plr.setHand('Gold', 'Silver', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.moat = self.g['Moat'].remove()
        self.plr.addCard(self.moat, 'hand')

    def test_playCard(self):
        self.plr.test_input = ['Trash Moat', 'Set Gold', 'Set Silver', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.g.inTrash('Moat'))
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertIsNotNone(self.plr.inHand('Silver'))
        self.assertIsNotNone(self.plr.inHand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
