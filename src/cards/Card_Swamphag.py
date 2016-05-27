#!/usr/bin/env python

import unittest
from Card import Card


class Card_Swamphag(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'duration']
        self.base = 'adventure'
        self.desc = """Until your next turn, when any other player buys a card, he gains a Curse.
        At the start of your next turn: +3 Coin"""
        self.needcurse = True
        self.name = 'Swamp Hag'
        self.cost = 5
        self.cost = 1

    def special(self, game, player):
        pass

    def duration(self, game, player):
        player.addCoin(3)

    def hook_allPlayers_buyCard(self, game, player, owner, card):
        if player == owner:
            return
        player.gainCard('Curse')
        player.output("Gained a curse from %s's Swamp Hag" % owner.name)
        owner.output("Cursed %s when they bought a %s" % (player.name, card.name))


###############################################################################
class Test_Swamphag(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Swamp Hag'])
        self.g.startGame()
        self.attacker, self.victim = self.g.playerList()
        self.seahag = self.g['Swamp Hag'].remove()
        self.attacker.addCard(self.seahag, 'hand')

    def test_play(self):
        self.attacker.playCard(self.seahag)
        self.attacker.endTurn()
        self.victim.buyCard(self.g['Copper'])
        self.assertEqual(self.attacker.durationpile[0].name, 'Swamp Hag')
        self.assertIsNotNone(self.victim.inDiscard('Curse'))
        self.attacker.startTurn()
        self.assertIsNotNone(self.attacker.inPlayed('Swamp Hag'))
        self.assertEquals(self.attacker.getCoin(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
