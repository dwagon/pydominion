#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Golem(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "Dig through deck for 2 action cards and play them"
        self.name = 'Golem'
        self.cost = 4
        self.potcost = 1

    def special(self, game, player):
        """ Reveal cards from your deck until you reveal 2 Action
            cards other than Golem cards. Discard the other cards, then
            play the Action cards in either order """
        actions = []
        maxnum = len(player.allCards())
        count = 0
        while len(actions) != 2:
            c = player.nextCard()
            count += 1
            if count > maxnum:
                player.output("Not enough action cards in deck")
                break
            if c.isAction() and c.name != 'Golem':
                player.pickupCard(card=c)
                actions.append(c)
            else:
                player.output("Drew and discarded %s" % c.name)
                player.discardCard(c)
        # TODO - let the player choose the order
        for card in actions:
            player.output("Playing %s" % c.name)
            player.playCard(card, costAction=False)


###############################################################################
class Test_Golem(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['golem', 'village', 'moat'])
        self.plr = self.g.playerList(0)
        self.card = self.g['golem'].remove()

    def test_actions(self):
        """ Ensure two actions are picked up and played, others are discarded """
        self.plr.setHand()
        self.plr.setDeck('gold', 'gold', 'gold', 'village', 'moat', 'estate', 'copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(['Golem', 'Moat', 'Village'], [c.name for c in self.plr.played])
        self.assertEqual(['Copper', 'Estate'], [c.name for c in self.plr.discardpile])

    def test_golem(self):
        """ Ensure golem isn't picked up """
        self.plr.setHand()
        self.plr.setDeck('gold', 'gold', 'gold', 'village', 'golem', 'moat', 'estate', 'copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(['Golem', 'Moat', 'Village'], [c.name for c in self.plr.played])
        self.assertEqual(['Copper', 'Estate', 'Golem'], [c.name for c in self.plr.discardpile])

    def test_nocards(self):
        self.plr.setHand('copper', 'copper', 'copper')
        self.plr.setDeck('copper', 'copper', 'copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
