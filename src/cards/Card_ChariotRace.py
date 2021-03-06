#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_ChariotRace(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.desc = """+1 Action
        Reveal the top card of your deck and put it into your hand.
        The player to your left reveals the top card of their deck.
        If your card costs more, +1 Coin and +1 VP"""
        self.name = 'Chariot Race'
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        card = player.pickupCard()
        player.revealCard(card)
        other = game.playerToLeft(player)
        othercard = other.nextCard()
        if card.cost > othercard.cost:
            player.output("Your %s costs more than %s's %s" % (card.name, other.name, othercard.name))
            player.addCoin()
            player.addScore('Chariot Race')
        else:
            player.output("Your %s costs less than %s's %s - Getting nothing" % (card.name, other.name, othercard.name))
        other.addCard(othercard, 'topdeck')


###############################################################################
class Test_ChariotRace(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Chariot Race'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Chariot Race'].remove()

    def test_play_win(self):
        """ Play a Chariot Race and win """
        self.plr.setDeck('Gold')
        self.vic.setDeck('Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertIsNotNone(self.plr.in_hand('Gold'))
        self.assertEqual(self.plr.score['Chariot Race'], 1)

    def test_play_lose(self):
        """ Play a Chariot Race and lose """
        self.plr.score['Chariot Race'] = 0
        self.plr.setDeck('Silver')
        self.vic.setDeck('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertIsNotNone(self.plr.in_hand('Silver'))
        self.assertEqual(self.plr.score['Chariot Race'], 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
