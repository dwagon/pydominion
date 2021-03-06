#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Rogue(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DARKAGES
        self.desc = """+2 coin; If there are any cards in the trash costing from 3 to
            6, gain one of them. Otherwise, each other player reveals
            the top 2 cards of his deck, trashes one of the costing
            from 3 to 6, and discards the rest """
        self.name = 'Rogue'
        self.coin = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        if not self.riffleTrash(game, player):
            self.rifflePlayers(game, player)

    ###########################################################################
    def rifflePlayers(self, game, player):
        for plr in player.attackVictims():
            self.riffleVictim(plr, player)

    ###########################################################################
    def riffleVictim(self, victim, player):
        cards = []
        for _ in range(2):
            c = victim.nextCard()
            victim.revealCard(c)
            if 3 <= c.cost <= 6:
                cards.append(c)
            else:
                victim.output("{}'s Rogue discarded {} as unsuitable".format(player.name, c.name))
                victim.addCard(c, 'discard')
        if not cards:
            player.output("No suitable cards from %s" % victim.name)
            return
        options = []
        index = 1
        for c in cards:
            sel = '%d' % index
            index += 1
            options.append({'selector': sel, 'print': 'Trash %s' % c.name, 'card': c})
        o = player.userInput(options, "Trash which card from %s?" % victim.name)
        victim.output("%s's rogue trashed your %s" % (player.name, o['card'].name))
        victim.trashCard(o['card'])
        # Discard what the rogue didn't trash
        for c in cards:
            if c != o['card']:
                victim.output("Rogue discarding %s as leftovers" % c.name)
                victim.discardCard(c)

    ###########################################################################
    def riffleTrash(self, game, player):
        options = []
        picked = set()
        index = 1
        for c in game.trashpile:
            if not c.insupply:
                continue
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
        player.output("Took a %s from the trash" % o['card'].name)
        return True


###############################################################################
class Test_Rogue(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Rogue', 'Moat'], badcards=['Pooka', 'Fool'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Rogue'].remove()

    def test_play(self):
        """ Nothing should happen """
        try:
            self.plr.addCard(self.card, 'hand')
            self.plr.playCard(self.card)
            self.assertEqual(self.plr.getCoin(), 2)
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_defended(self):
        """ Victim has a defense """
        self.plr.hand.empty()
        self.plr.addCard(self.card, 'hand')
        moat = self.g['Moat'].remove()
        self.victim.addCard(moat, 'hand')
        self.plr.playCard(self.card)

    def test_good_trash(self):
        """ Rogue to get something juicy from the trash """
        tsize = self.g.trashSize()
        for _ in range(2):
            gold = self.g['Gold'].remove()
            self.plr.trashCard(gold)
        self.plr.test_input = ['1']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.g.trashSize(), tsize + 1)
            self.assertEqual(self.plr.discardpile.size(), 1)
            self.assertEqual(self.plr.discardpile[-1].name, 'Gold')
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_good_player(self):
        """ Rogue to trash something from another player """
        tsize = self.g.trashSize()
        self.victim.setDeck('Gold', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash('Duchy'))
        self.assertEqual(self.victim.discardpile.size(), 1)
        self.assertEqual(self.victim.discardpile[-1].name, 'Gold')

    def test_bad_player(self):
        """ Rogue to trash nothing from another player """
        tsize = self.g.trashSize()
        self.victim.setDeck('Gold', 'Province', 'Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize)
        self.assertEqual(self.victim.discardpile.size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
