#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Advisor(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = "+1 action, +3 cards, plr to left discards one of them"
        self.name = 'Advisor'
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Reveal the top 3 cards of your deck. The player to your
            left chooses one of them. Discard that card. Put
            the other cards into your hand. """
        cards = []
        choser = game.playerToLeft(player)
        for i in range(3):
            card = player.pickupCard()
            player.revealCard(card)
            cards.append(card)
        to_discard = choser.cardSel(
                    force=True,
                    prompt='Pick a card of %s to discard from Advisor' % player.name,
                    cardsrc=cards,
                    verbs=('Discard', 'Undiscard')
                    )[0]
        player.output("%s discarded %s" % (choser.name, to_discard.name))
        player.discardCard(to_discard)


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):  # pragma: no cover
    # Discard the card that costs the most
    cardlist = [(c.cost, c) for c in kwargs['cardsrc'] if c.isTreasure()]
    if cardlist:
        most = sorted(cardlist)[-1]
        if most:
            return [most[1]]
    cardlist = [(c.cost, c) for c in kwargs['cardsrc'] if c.isAction()]
    if cardlist:
        most = sorted(cardlist)[-1]
        if most:
            return [most[1]]
    cardlist = [(c.cost, c) for c in kwargs['cardsrc']]
    most = sorted(cardlist)[-1]
    return [most[1]]


###############################################################################
class Test_Advisor(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Advisor'])
        self.g.startGame()
        self.plr, self.plr2 = self.g.playerList()
        self.acard = self.g['Advisor'].remove()
        self.plr.addCard(self.acard, 'hand')

    def test_play(self):
        """" Play an advisor """
        self.plr.setDeck('Duchy', 'Silver', 'Gold')
        self.plr2.test_input = ['discard gold']
        self.plr.playCard(self.acard)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 3 - 1)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNone(self.plr.inHand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
