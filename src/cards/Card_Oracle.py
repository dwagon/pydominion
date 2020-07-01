#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Oracle(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'hinterlands'
        self.desc = """Each player (including you) reveals the top 2 cards of his deck, and you choose one:
        either he discards them or he puts them back on top in an order he chooses.  +2 cards """
        self.name = 'Oracle'
        self.cost = 3

    def special(self, game, player):
        for plr in player.attackVictims():
            self.attack(player, plr, "%s's" % plr.name)
        self.attack(player, player, "your")
        player.pickupCards(2)

    def attack(self, player, victim, name):
        cards = []
        for _ in range(2):
            card = victim.nextCard()
            victim.revealCard(card)
            cards.append(card)
        cardnames = ", ".join([c.name for c in cards])
        discard = player.plrChooseOptions(
            "What to do with %s cards: %s" % (name, cardnames),
            ("Discard %s" % cardnames, True),
            ("Put %s on top of deck" % cardnames, False))
        if discard:
            for card in cards:
                victim.discardCard(card)
            victim.output("%s's Oracle discarded your %s" % (player.name, cardnames))
        else:
            for card in cards:
                victim.addCard(card, 'topdeck')
            victim.output("%s's Oracle put %s on top of your deck" % (player.name, cardnames))


###############################################################################
class Test_Oracle(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Oracle'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Oracle'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_card(self):
        """ Play Oracle """
        self.vic.setDeck('Estate', 'Duchy', 'Province')
        self.plr.setDeck('Copper', 'Silver', 'Gold')
        self.plr.test_input = ['discard', 'top']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.vic.inDiscard('Duchy'))
        self.assertIsNotNone(self.vic.inDiscard('Province'))
        self.assertIsNotNone(self.plr.inHand('Silver'))
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertEqual(self.plr.handSize(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
