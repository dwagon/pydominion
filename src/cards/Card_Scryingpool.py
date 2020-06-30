#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Scryingpool(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'alchemy'
        self.desc = """+1 Action. Each player (including you) reveals the top card of
        his deck and either discards it or puts it back, your choice.
        Then reveal cards from the top of your deck until you reveal one that is not an Action.
        Put all of your revealed cards into your hand."""
        self.name = 'Scrying Pool'
        self.actions = 1
        self.cost = 2
        self.required_cards = ['Potion']
        self.potcost = True

    def special(self, game, player):
        for plr in player.attackVictims():
            self.discardOrPutBack(plr, player)
        self.discardOrPutBack(player, player)
        revealed = []
        while True:
            topcard = player.pickupCard()
            player.revealCard(topcard)
            if not topcard.isAction():
                break
            revealed.append(topcard)
        for card in revealed:
            player.addCard(card, 'hand')

    def discardOrPutBack(self, victim, player):
        if player == victim:
            name = ("you", "your")
        else:
            name = (victim.name, "%s's" % victim.name)
        topcard = victim.nextCard()
        victim.revealCard(topcard)
        putback = player.plrChooseOptions(
            "For %s which one?" % name[0],
            ('Discard %s' % topcard.name, False),
            ('Putback %s' % topcard.name, True))
        if putback:
            victim.output("Put %s back on %s deck" % (topcard.name, name[1]))
            victim.addCard(topcard, 'deck')
        else:
            victim.output("Discarded %s" % topcard.name)
            victim.addCard(topcard, 'discard')


###############################################################################
class Test_ScryingPool(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Scrying Pool', 'Moat'])
        self.g.start_game()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Scrying Pool'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a scrying pool """
        self.plr.setDeck('Moat', 'Gold')
        self.vic.setDeck('Duchy')
        self.plr.test_input = ['discard', 'putback']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.vic.inDiscard('Duchy'))
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertIsNotNone(self.plr.inHand('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
# EOF
