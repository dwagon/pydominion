#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Gladiator(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'empires'
        self.desc = """+2 Coin
        Reveal a card from your hand. The player to your left may reveal a copy from their hand.
        If they do not, +1 Coin and trash a Gladiator from the Supply."""
        self.name = 'Gladiator'
        self.cost = 3
        self.coin = 2
        self.numcards = 5
        self.split = 'Fortune'

    def special(self, game, player):
        mycard = player.cardSel(
            num=1, force=True,
            prompt="Select a card from your hand that the player to your left doesn't have")
        player.revealCard(mycard[0])
        lefty = game.playerToLeft(player)
        leftycard = lefty.inHand(mycard[0].name)
        if not leftycard:
            player.output("%s doesn't have a %s" % (lefty.name, mycard[0].name))
            player.addCoin(1)
            c = game['Gladiator'].remove()
            player.trashCard(c)
        else:
            player.output("%s has a %s" % (lefty.name, mycard[0].name))
            lefty.revealCard(leftycard)


###############################################################################
class Test_Gladiator(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Gladiator', 'Moat'])
        self.g.start_game()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Gladiator'].remove()

    def test_play_nothave(self):
        """ Play a Gladiator - something the other player doesn't have """
        self.plr.setHand('Moat', 'Copper', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Moat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.inTrash('Gladiator'))
        self.assertEqual(self.plr.getCoin(), 3)

    def test_play_has(self):
        """ Play a Gladiator - something the other player has """
        self.plr.setHand('Moat', 'Copper', 'Estate')
        self.vic.setHand('Moat', 'Copper', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Moat']
        self.plr.playCard(self.card)
        self.assertIsNone(self.g.inTrash('Gladiator'))
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
