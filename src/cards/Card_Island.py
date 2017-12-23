#!/usr/bin/env python

from Card import Card
import unittest
from PlayArea import PlayArea


###############################################################################
class Card_Island(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'victory']
        self.base = 'seaside'
        self.desc = """Set aside this and another card from your hand. Return them to your deck at the end of the game.  2VP"""
        self.name = 'Island'
        self.cost = 4
        self.victory = 2

    def special(self, game, player):
        if not hasattr(player, 'island_reserve'):
            player.island_reserve = PlayArea([])
        c = player.cardSel(prompt="Select a card to set aside for the rest of the game")
        if c:
            card = c[0]
            player.island_reserve.add(card)
            player.end_of_game_cards.append(card)
            player.hand.remove(card)
            player.secret_count += 1
        player.played.remove(self)
        player.end_of_game_cards.append(self)
        player.island_reserve.add(self)
        player.secret_count += 1

    def hook_end_of_game(self, game, player):
        for card in player.island_reserve[:]:
            player.output("Returning %s from Island" % card.name)
            player.addCard(card)
            player.island_reserve.remove(card)


###############################################################################
class Test_Island(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Island'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Island'].remove()

    def test_play_province(self):
        """ Play an island on a province """
        self.plr.setHand('Silver', 'Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['province']
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.inPlayed('Island'))
        self.assertIsNone(self.plr.inHand('Island'))
        self.assertIsNone(self.plr.inDiscard('Island'))
        self.assertIsNone(self.plr.inHand('Province'))
        self.assertIsNone(self.plr.inDiscard('Province'))
        self.assertEqual(self.plr.secret_count, 2)
        self.plr.gameOver()
        self.assertIsNotNone(self.plr.inDiscard('Island'))
        self.assertIsNotNone(self.plr.inDiscard('Province'))
        score = self.plr.getScoreDetails()
        self.assertEqual(score['Island'], 2)
        self.assertEqual(score['Province'], 6)

    def test_play_alone(self):
        """ Play a island but don't pick another card"""
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['finish']
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.inPlayed('Island'))
        self.assertIsNone(self.plr.inHand('Island'))
        self.assertIsNone(self.plr.inDiscard('Island'))
        self.assertEqual(self.plr.secret_count, 1)
        self.plr.gameOver()
        self.assertIsNotNone(self.plr.inDiscard('Island'))
        score = self.plr.getScoreDetails()
        self.assertEqual(score['Island'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
