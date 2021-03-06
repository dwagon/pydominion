#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Saboteur(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.INTRIGUE
        self.desc = """Each other player reveals cards from the top of his deck
            until revealing one costing 3 Coin or more. He trashes that card
            and may gain a card costing at most 2 Coin less than it. He discards
            the revealed cards."""
        self.name = 'Saboteur'
        self.cost = 5

    def special(self, game, player):
        """ Each other player reveals cards from the top of his
            deck until revealing one costing 3 or more. He trashes that
            card and may gain a card costing at most 2 less than it.
            He discards the other revealed cards. """
        for victim in player.attackVictims():
            card = self.pickCard(victim, player)
            if not card:
                continue
            victim.output("%s's saboteur trashed %s" % (player.name, card.name))
            victim.trashCard(card)
            victim.plrGainCard(card.cost - 2)

    def pickCard(self, victim, player):
        for _ in range(len(victim.allCards())):
            c = victim.nextCard()
            victim.revealCard(c)
            if c.cost >= 3:
                return c
            victim.output("Saboteur checking and discarding %s" % c.name)
            victim.discardCard(c)
        victim.output("Don't have any suitable cards")
        player.output("%s doesn't have any suitable cards")
        return None


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):      # pragma: no coverage
    toget = []
    for card in kwargs['cardsrc']:
        if card.name in ('Copper', 'Silver', 'Gold'):
            toget.append((card.cost, card))
    if toget:
        return [sorted(toget)[-1][1]]
    return []


###############################################################################
class Test_Saboteur(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=2,
            initcards=['Saboteur'],
            badcards=['Blessed Village', 'Cemetery', 'Necromancer', 'Animal Fair']
        )
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Saboteur'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a saboteur """
        tsize = self.g.trashSize()
        try:
            self.victim.test_input = ['Get Estate']
            self.victim.setDeck('Gold', 'Copper', 'Estate')
            self.plr.playCard(self.card)
            self.assertEqual(self.g.trashSize(), tsize + 1)
            trashed = self.g.trashpile[0]
            self.assertTrue(trashed.cost >= 3)
            for c in self.victim.discardpile[:-1]:
                self.assertTrue(c.cost < 3)
            self.assertTrue(self.victim.discardpile[-1].cost <= trashed.cost - 2)
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_nomatching(self):
        """ Play a saboteur where the victim doesn't have a suitable card """
        tsize = self.g.trashSize()
        self.victim.setDeck('Copper', 'Copper', 'Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize)
        for c in self.victim.discardpile:
            self.assertTrue(c.cost < 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
