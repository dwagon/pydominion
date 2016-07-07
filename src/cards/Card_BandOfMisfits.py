#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_BandOfMisfits(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """Play this as if it were an Action card in the Supply costing less than it that you choose. This is that card until it leaves play."""
        self.name = 'Band of Misfits'
        self.cost = 5

    def special(self, game, player):
        actionpiles = game.getActionPiles(self.cost - 1)
        actions = player.cardSel(
            prompt="What action card do you want to imitate?",
            cardsrc=actionpiles)
        self._action = actions[0]
        player.addActions(self._action.actions)
        player.addBuys(self._action.buys)
        player.addCoin(self._action.coin)
        player.pickupCards(self._action.cards)
        self._action.special(game, player)

    def hook_endTurn(self, game, player):
        if not hasattr(self, '_action'):
            return
        del self._action

    def hook_discardCard(self, game, player):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_discardCard(game, player)

    def hook_allPlayers_buyCard(self, game, player, owner, card):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_allPlayers_buyCard(game, player, owner, card)

    def hook_allPlayers_gainCard(self, game, player, owner, card):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_allPlayers_gainCard(game, player, owner, card)

    def hook_buyCard(self, game, player, card):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_buyCard(game, player, card)

    def hook_callReserve(self, game, player):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_callReserve(game, player)

    def hook_cardCost(self, game, player, card):
        if not hasattr(self, '_action'):
            return 0
        return self._action.hook_cardCost(game, player, card)

    def hook_cleanup(self, game, player):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_cleanup(game, player)

    def hook_gainCard(self, game, player, card):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_gainCard(game, player, card)

    def hook_postAction(self, game, player):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_postAction(game, player)

    def hook_spendValue(self, game, player, card):
        if not hasattr(self, '_action'):
            return 0
        return self._action.hook_spendValue(game, player, card)

    def hook_trashCard(self, game, player, card):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_trashCard(game, player, card)

    def hook_trashThisCard(self, game, player):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_trashThisCard(game, player)

    def hook_trashcard(self, game, player):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_trashcard(game, player)

    def hook_underAttack(self, player, game):
        if not hasattr(self, '_action'):
            return
        return self._action.hook_underAttack(player, game)


###############################################################################
class Test_BandOfMisfits(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Band of Misfits', 'Feast', 'Bureaucrat', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Band of Misfits'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_market(self):
        """ Make the Band of Misfits be a Bureaucrat """
        self.plr.test_input = ['Bureaucrat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDeck('Silver'))

    def test_play_feast(self):
        """ Make the Band of Misfits be a Feast """
        self.plr.test_input = ['Feast', 'trash', 'moat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF