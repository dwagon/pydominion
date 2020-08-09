#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Thief(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.ATTACK]
        self.base = Game.DOMINION
        self.desc = """Each other player reveals the top 2 cards of his deck.
            If they revealed any Treasure cards, they trash one of them that you choose.
            You may gain any or all of these trashed cards. They discard the other revealed cards."""
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
        for _ in range(2):
            c = victim.nextCard()
            victim.revealCard(c)
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
                thief.output("Trashed %s from %s" % (o['card'].name, victim.name))
                victim.output("%s trashed your %s" % (thief.name, o['card'].name))


###############################################################################
class Test_Thief(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Thief', 'Moat'])
        self.g.start_game()
        self.thiefcard = self.g['Thief'].remove()
        self.thief, self.victim = self.g.player_list()
        self.thief.name = 'thief'
        self.victim.name = 'victim'
        self.thief.addCard(self.thiefcard, 'hand')

    def test_no_treasure(self):
        self.victim.setDeck('Estate', 'Estate', 'Estate')
        self.thief.playCard(self.thiefcard)
        self.assertIn('Player victim has no treasures', self.thief.messages)

    def test_moat_defense(self):
        self.victim.setHand('Moat', 'Copper', 'Copper')
        self.victim.setDeck('Copper', 'Silver', 'Gold')
        self.thief.playCard(self.thiefcard)
        self.assertIn('Player victim is defended', self.thief.messages)
        self.assertEqual(self.victim.deckSize(), 3)
        self.assertEqual(self.victim.discard_size(), 0)

    def test_do_nothing(self):
        self.victim.setHand('Copper', 'Copper')
        self.victim.setDeck('Copper', 'Silver', 'Gold')
        self.thief.test_input = ["Don't trash"]
        self.thief.playCard(self.thiefcard)
        self.assertEqual(self.victim.deckSize(), 1)
        self.assertEqual(self.victim.discard_size(), 2)
        self.assertEqual(self.thief.discard_size(), 0)

    def test_trash_treasure(self):
        self.victim.setHand('Copper', 'Copper')
        self.victim.setDeck('Copper', 'Silver', 'Gold')
        self.thief.test_input = ['trash gold']
        self.thief.playCard(self.thiefcard)
        # Make sure the gold ends up in the trashpile and not in the victims deck
        self.assertIsNotNone(self.g.in_trash('Gold'))
        for c in self.victim.deck:
            self.assertNotEqual(c.name, 'Gold')
        self.assertEqual(self.victim.discardpile[0].name, 'Silver')

    def test_steal_treasure(self):
        tsize = self.g.trashSize()
        self.victim.setHand('Copper', 'Copper')
        self.victim.setDeck('Copper', 'Silver', 'Gold')
        self.thief.test_input = ['steal gold']
        self.thief.playCard(self.thiefcard)
        self.assertEqual(self.g.trashSize(), tsize)
        for c in self.victim.deck:
            self.assertNotEqual(c.name, 'Gold')
        for c in self.thief.discardpile:
            if c.name == 'Gold':
                break
        else:   # pragma: no cover
            self.fail()
        self.assertIn('%s stole your Gold' % self.thief.name, self.victim.messages)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
