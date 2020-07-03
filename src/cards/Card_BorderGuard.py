#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_BorderGuard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.desc = """+1 Action; Reveal the top 2 cards of your deck.
        Put one into your hand and discard the other. If both were Actions,
        take the Lantern or Horn."""
        self.name = 'Border Guard'
        self.cost = 2
        self.actions = 1

    def special(self, game, player):
        ncards = 3 if player.has_artifact('Lantern') else 2
        cards = []
        for _ in range(ncards):
            card = player.nextCard()
            player.revealCard(card)
            cards.append(card)
        nacts = sum([1 for _ in cards if _.isAction()])
        ch = player.cardSel(
            prompt="Select a card to put into your hand, other will be discarded",
            cardsrc=cards
        )
        player.addCard(ch[0], 'hand')
        cards.remove(ch[0])
        for card in cards:
            player.output("Putting {} into the discard pile".format(card.name))
            player.addCard(card, 'discard')

        if nacts == ncards:
            art = player.plrChooseOptions(
                "Pick an artifact to take",
                ("Take Lantern (Border Guard reveals 3 cards)", 'Lantern'),
                ("Take Horn (May put discarded Border Guard into hand)", 'Horn')
            )
            player.assign_artifact(art)

    def hook_discardThisCard(self, game, player, source):
        if not player.has_artifact('Horn'):
            return
        ch = player.plrChooseOptions(
            "Use Horn and put Border Guard into hand?",
            ("Put into hand", True),
            ("Keep in discard", False)
        )
        if ch:
            player.addCard(self, 'topdeck')
            player.discardpile.remove(self)


###############################################################################
class Test_BorderGuard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Border Guard', 'Moat', 'Guide'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Border Guard'].remove()

    def test_play(self):
        self.plr.setDeck('Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Select Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Silver'))

    def test_play_actions(self):
        self.plr.setDeck('Moat', 'Guide')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Select Moat', 'Take Horn']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inHand('Moat'))
        self.assertIsNotNone(self.plr.inDiscard('Guide'))
        self.assertTrue(self.plr.has_artifact('Horn'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF