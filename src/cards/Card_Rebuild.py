#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Rebuild(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """+1 action. Name a card. Reveal cards from the top
        of your deck until you reveal a Victory card that is
        not the named card.  Discard the other cards.
        Trash the Victory card and gain a Victory card cost up to 3 more than it"""
        self.name = 'Rebuild'
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """ Name a card. Reveal cards from the top of your deck
            until you reveal a Victory card that is not the named card.
            Discard the other cards. Trash the Victory card and gain a
            Victory card cost up to 3 more than it"""
        stacks = game.getVictoryPiles()
        cards = player.cardSel(
            prompt="Guess a victory card - the next victory card that is not that will be upgraded",
            cardsrc=stacks,
            )
        if cards:
            guess = cards[0]
        else:
            return
        discards = []
        while True:
            card = player.nextCard()
            player.revealCard(card)
            if not card:
                break
            if card.isVictory() and guess.name != card.name:
                player.output("Found and trashing a %s" % card.name)
                player.trashCard(card)
                player.plrGainCard(card.cost + 3, modifier='less', types={'victory': True})
                break
            else:
                player.output("Drew and discarded %s" % card.name)
                discards.append(card)
        for c in discards:
            player.discardCard(c)


###############################################################################
class Test_Rebuild(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Rebuild'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Rebuild'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a rebuild """
        tsize = self.g.trashSize()
        self.plr.setDeck('Copper', 'Copper', 'Estate', 'Province', 'Gold')
        self.plr.test_input = ['Select Province', 'Get Duchy']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.discardSize(), 3)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Province'))
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.inTrash('Estate'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
