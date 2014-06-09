#!/usr/bin/env python

from Card import Card
import unittest


class Card_Thief(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'dominion'
        self.desc = "Steal treasure from other players"
        self.name = 'Thief'
        self.cost = 4

    def special(self, game, player):
        """ Each other player reveals the top 2 cards of his deck.
            If they revealed any Treasure cards, they trash one them
            that you choose. You may gain any or all of these trashed
            Cards. They discard the other revealed cards. """

        for pl in player.attackVictims():
            self.thieveOn(pl, player)

    def thieveOn(self, victim, thief):
        treasures = []
        for i in range(2):
            c = victim.nextCard()
            if c.isTreasure():
                treasures.append(c)
            else:
                victim.addCard(c, 'discard')
        if not treasures:
            thief.output("Player %s has no treasures" % victim.name)
            return
        index = 1
        options = [{'selector': '0', 'print': "Don't trash any card", 'card': None, 'steal': False}]
        for c in treasures:
            sel = '%s' % index
            pr = "Trash %s from %s" % (c.name, victim.name)
            options.append({'selector': sel, 'print': pr, 'card': c, 'steal': False})
            index += 1
            sel = '%s' % index
            pr = "Steal %s from %s" % (c.name, victim.name)
            options.append({'selector': sel, 'print': pr, 'card': c, 'steal': True})
            index += 1
        o = thief.userInput(options, "What to do to %s's cards?" % victim.name)
        # Discard the ones we don't care about
        for tc in treasures:
            if o['card'] != tc:
                victim.addCard(tc, 'discard')
        if o['card']:
            if o['steal']:
                thief.addCard(o['card'])
                thief.output("Stealing %s from %s" % (o['card'].name, victim.name))
                victim.output("%s stole your %s" % (thief.name, o['card'].name))
            else:
                victim.trashCard(o['card'])


###############################################################################
class Test_Thief(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['thief', 'moat'], playernames=['victim', 'thief'])
        self.thiefcard = self.g['thief'].remove()
        self.thief = self.g.players[0]
        self.thief.addCard(self.thiefcard, 'hand')
        self.victim = self.g.players[1]

    def test_no_treasure(self):
        self.victim.setDeck('estate', 'estate', 'estate')
        self.thief.playCard(self.thiefcard)
        self.assertIn('Player victim has no treasures', self.thief.messages)

    def test_moat_defense(self):
        self.victim.setHand('moat', 'copper', 'copper')
        self.victim.setDeck('copper', 'silver', 'gold')
        self.thief.playCard(self.thiefcard)
        self.assertIn('Player victim is defended', self.thief.messages)
        self.assertEquals(len(self.victim.deck), 3)
        self.assertEquals(len(self.victim.discardpile), 0)

    def test_do_nothing(self):
        self.victim.setHand('copper', 'copper')
        self.victim.setDeck('copper', 'silver', 'gold')
        self.thief.test_input = ['0']
        self.thief.playCard(self.thiefcard)
        self.assertEquals(len(self.victim.deck), 1)
        self.assertEquals(len(self.victim.discardpile), 2)
        self.assertEquals(len(self.thief.discardpile), 0)

    def test_trash_treasure(self):
        self.victim.setHand('copper', 'copper')
        self.victim.setDeck('copper', 'silver', 'gold')
        self.thief.test_input = ['1']
        self.thief.playCard(self.thiefcard)
        # Make sure the gold ends up in the trashpile and not in the victims deck
        self.assertEquals(self.g.trashpile[0].name, 'Gold')
        for c in self.victim.deck:
            self.assertNotEquals(c.name, 'Gold')
        self.assertEquals(self.victim.discardpile[0].name, 'Silver')

    def test_steal_treasure(self):
        self.victim.setHand('copper', 'copper')
        self.victim.setDeck('copper', 'silver', 'gold')
        self.thief.test_input = ['2']
        self.thief.playCard(self.thiefcard)
        self.assertEquals(self.g.trashpile, [])
        for c in self.victim.deck:
            self.assertNotEquals(c.name, 'Gold')
        for c in self.thief.discardpile:
            if c.name == 'Gold':
                break
        else:   # pragma: no cover
            self.fail()
        self.assertIn('%s stole your Gold' % self.thief.name, self.victim.messages)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
