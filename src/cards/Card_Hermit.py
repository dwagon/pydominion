#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Hermit(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DARKAGES
        self.desc = """Look through your discard pile. You may trash a card from
            your discard pile or hand that is not a Treasure.  Gain a card
            costing up to 3.  When you discard this from play, if you did not
            buy any cards this turn, trash this and gain a Madman from the Madman pile."""
        self.name = 'Hermit'
        self.required_cards = [('Card', 'Madman')]
        self.cost = 3

    def special(self, game, player):
        # Look through your discard pile. You may trash a card from your
        # discard pile or hand that is not a Treasure.
        to_trash = []
        for card in player.discardpile + player.hand:
            if not card.isTreasure():
                to_trash.append(card)
        choice = player.cardSel(
            prompt="Trash one of these?",
            cardsrc=to_trash,
            verbs=('Trash', 'Untrash')
            )
        if choice:
            if player.in_discard(choice[0].name):
                player.discardpile.remove(choice[0])
            else:
                player.hand.remove(choice[0])
            player.trashCard(choice[0])
        # Gain a card costing up to 3.
        player.plrGainCard(3)

    def hook_discardThisCard(self, game, player, source):
        # When you discard this from play, if you did not buy any cards this turn,
        # trash this and gain a Madman from the Madman pile
        if not player.stats['bought']:
            trash = player.plrChooseOptions(
                "Trash this to gain a madman",
                ("Keep Hermit", False),
                ("Gain Madman", True))
            if trash:
                player.trashCard(self)
                player.gainCard('Madman')


###############################################################################
class Test_Hermit(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hermit'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Hermit'].remove()

    def test_play_discard(self):
        """ Play a Hermit trashing card from discard """
        self.plr.setDiscard('Province', 'Gold')
        self.plr.test_input = ['trash province', 'get silver']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Province'))
        self.assertIsNone(self.plr.in_discard('Province'))
        self.assertIsNotNone(self.plr.in_discard('Silver'))

    def test_play_hand(self):
        """ Play a Hermit trashing card from hand """
        self.plr.setHand('Province')
        self.plr.test_input = ['trash province', 'get silver']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Province'))
        self.assertIsNone(self.plr.in_hand('Province'))
        self.assertIsNotNone(self.plr.in_discard('Silver'))

    def test_discard(self):
        """ Discard a Hermit and gain a Madman """
        self.plr.test_input = ['madman']
        self.plr.addCard(self.card, 'hand')
        self.plr.discardHand()
        self.assertIsNotNone(self.plr.in_discard('Madman'))
        self.assertIsNone(self.plr.in_hand('Hermit'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
