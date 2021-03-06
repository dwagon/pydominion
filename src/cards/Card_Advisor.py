#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Advisor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.GUILDS
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
        for _ in range(3):
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
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
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
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Advisor'])
        self.g.start_game()
        self.plr, self.plr2 = self.g.player_list()
        self.acard = self.g['Advisor'].remove()
        self.plr.addCard(self.acard, 'hand')

    def test_play(self):
        """" Play an advisor """
        self.plr.setDeck('Duchy', 'Silver', 'Gold')
        self.plr2.test_input = ['discard gold']
        self.plr.playCard(self.acard)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 3 - 1)
        self.assertIsNotNone(self.plr.in_discard('Gold'))
        self.assertIsNone(self.plr.in_hand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
