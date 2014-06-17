#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Rogue(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'darkages'
        self.desc = "Pull a card from the trash or attack other player hands"
        self.name = 'Rogue'
        self.gold = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        """ If there are any cards in the trash costing from 3 to
            6, gain one of them. Otherwise, each other player reveals
            the top 2 cards of his deck, trashes one of the costing
            from 3 to 6, and discards the rest """
        if not self.riffleTrash(game, player):
            self.rifflePlayers(game, player)

    ###########################################################################
    def rifflePlayers(self, game, player):
        for plr in player.attackVictims():
            self.riffleVictim(plr, player)

    ###########################################################################
    def riffleVictim(self, victim, player):
        cards = []
        for i in range(2):
            c = victim.nextCard()
            if 3 <= c.cost <= 6:
                cards.append(c)
            else:
                victim.addCard(c, 'discard')
        if not cards:
            return
        options = []
        index = 1
        for c in cards:
            sel = '%d' % index
            index += 1
            options.append({'selector': sel, 'print': 'Trash %s' % c.name, 'card': c})
        o = player.userInput(options, "Trash which card from %s" % victim.name)
        victim.output("%s's rogue trashed your %s" % (player.name, o['card'].name))
        victim.trashCard(o['card'])

    ###########################################################################
    def riffleTrash(self, game, player):
        options = []
        picked = set()
        index = 1
        for c in game.trashpile:
            if c.name in picked:
                continue
            if 3 <= c.cost <= 6:
                picked.add(c.name)
                sel = '%d' % index
                index += 1
                options.append({'selector': sel, 'print': 'Take %s' % c.name, 'card': c})
        if index == 1:
            return False
        o = player.userInput(options, "Pick a card from the trash")
        game.trashpile.remove(o['card'])
        player.addCard(o['card'])
        return True


###############################################################################
class Test_Rogue(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['rogue', 'moat'])
        self.plr, self.victim = self.g.players.values()
        self.card = self.g['rogue'].remove()

    def test_play(self):
        """ Nothing should happen """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['gold'], 2)

    def test_defended(self):
        """ Victim has a defense """
        self.plr.hand = []
        self.plr.addCard(self.card, 'hand')
        moat = self.g['moat'].remove()
        self.victim.addCard(moat, 'hand')
        self.plr.playCard(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
