#!/usr/bin/env python

from Card import Card
from CardPile import CardPile
import random
import unittest


###############################################################################
class Card_Knight(Card):
    def __init__(self):
        Card.__init__(self)
        self.name = 'Knight'

    def setup(self, game):
        game.cardpiles['Knight'] = KnightCardPile(game.cardmapping['KnightCard'])


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class KnightCardPile(CardPile):
    def __init__(self, mapping, pilesize=10):
        self.pilesize = pilesize
        self.embargo_level = 0
        knighttypes = mapping

        self.knights = [c() for c in knighttypes.values()]
        random.shuffle(self.knights)

    def __getattr__(self, key):
        try:
            if key == 'card':
                return self.knights[-1]
            return getattr(self.knights[-1], key)
        except IndexError:
            return None

    def remove(self):
        if self.pilesize:
            self.pilesize -= 1
            return self.knights.pop()
        else:
            return None

    def __repr__(self):
        return "KnightCardPile %s: %d" % (self.name, self.pilesize)


###############################################################################
class KnightCard(Card):
    def knight_special(self, game, player):
        """ Each other player reveals the top 2 cards of his deck,
            trashes one of them costing from 3 to 6 and discards the
            rest. If a knight is trashed by this, trash this card """
        for pl in player.attackVictims():
            self.knight_attack(game, player, pl)

    def knight_attack(self, game, player, victim):
        cards = []
        for i in range(2):
            c = victim.nextCard()
            victim.revealCard(c)
            if c.cost in (3, 4, 5, 6):
                cards.append(c)
            else:
                victim.output("%s's %s discarded your %s" % (player.name, self.name, c.name))
                victim.discardCard(c)
        if not cards:
            return
        player.output("Looking at %s" % ", ".join([x.name for x in cards]))

        trash = victim.plrTrashCard(cardsrc=cards, force=True, prompt="%s's %s trashes one of your cards" % (player.name, self.name))
        to_trash = trash[0]
        player.output("%s trashed a %s" % (victim.name, to_trash.name))

        if to_trash.isKnight():
            player.output("%s trashed a knight: %s - trashing your %s" % (victim.name, to_trash.name, self.name))
            player.trashCard(self)
        for c in cards:

            if c != to_trash:
                victim.output("%s's %s discarded your %s" % (player.name, self.name, c.name))
                victim.discardCard(c)


###############################################################################
class Test_Knight(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Knight'])
        self.g.start_game()
        self.plr, self.vic = self.g.playerList()
        self.card = None
        self.card = self.g['Knight'].remove()

        # Makes testing harder due to card actions
        while self.card.name in ('Dame Anna', 'Dame Natalie', 'Sir Michael'):
            self.card = self.g['Knight'].remove()

        self.plr.setHand('Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')

    def test_playcard_nosuitable(self):
        """ Play a knight woth no suitable cards"""
        self.vic.setDeck('Copper', 'Copper')
        self.plr.playCard(self.card)
        self.assertEqual(self.vic.discardSize(), 2)

    def test_playcard_one_suitable(self):
        """ Play a knight with one suitable card """
        self.vic.setDeck('Copper', 'Duchy')
        self.vic.test_input = ['Duchy']
        self.plr.playCard(self.card)
        self.assertEqual(self.vic.discardSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
