#!/usr/bin/env python

import unittest
from Card import Card
from PlayArea import PlayArea


###############################################################################
class Card_Crypt(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'duration']
        self.base = 'nocturne'
        self.desc = "Set aside any number of Treasures you have in play, face down (under this). While any remain, at the start of each of your turns, put one of them into your hand."
        self.name = 'Crypt'
        self.cost = 5

    def night(self, game, player):
        if not hasattr(player, '_crypt_reserve'):
            player._crypt_reserve = PlayArea([])
        cards = player.cardSel(
            prompt='Set aside any number of Treasures you have in play',
            verbs=('Set', 'Unset'),
            anynum=True,
            types={'treasure': True},
            cardsrc='played'
                )
        if cards:
            for card in cards:
                player._crypt_reserve.add(card)
                player.played.remove(card)
                player.secret_count += 1
            self.permanent = True

    def duration(self, game, player):
        options = []
        index = 0
        for card in player._crypt_reserve:
            sel = "{}".format(index)
            toprint = "Bring back {}".format(card.name)
            options.append({'selector': sel, 'print': toprint, 'card': card})
            index += 1
        o = player.userInput(options, "What card to bring back from the crypt?")
        player.addCard(o['card'], 'hand')
        player._crypt_reserve.remove(o['card'])
        player.secret_count -= 1
        if player._crypt_reserve.isEmpty():
            self.permanent = False


###############################################################################
class Test_Crypt(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Crypt'], badcards=['Duchess'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Crypt'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.phase = 'night'
        self.plr.setPlayed('Silver', 'Gold', 'Estate')
        self.plr.test_input = ['Set Gold', 'Set Silver', 'Finish']
        self.plr.playCard(self.card)
        self.plr.endTurn()
        self.plr.test_input = ['Bring back Gold']
        self.plr.startTurn()
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertEqual(len(self.plr._crypt_reserve), 1)
        self.plr.endTurn()
        self.plr.test_input = ['Bring back Silver']
        self.plr.startTurn()
        self.assertIsNotNone(self.plr.inHand('Silver'))
        self.assertFalse(self.card.permanent)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
