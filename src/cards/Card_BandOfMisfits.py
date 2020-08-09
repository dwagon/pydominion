#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_BandOfMisfits(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DARKAGES
        self.desc = """Play this as if it were an Action card in the Supply
            costing less than it that you choose. This is that card until it
            leaves play."""
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

    def hook_end_turn(self, game, player):
        if not hasattr(self, '_action'):
            return
        del self._action

    def hook_discardThisCard(self, game, player, source):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_discardThisCard(game, player, source)

    def hook_allPlayers_buyCard(self, game, player, owner, card):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_allPlayers_buyCard(game, player, owner, card)

    def hook_allplayers_gain_card(self, game, player, owner, card):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_allplayers_gain_card(game, player, owner, card)

    def hook_buyCard(self, game, player, card):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_buyCard(game, player, card)

    def hook_call_reserve(self, game, player):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_call_reserve(game, player)

    def hook_cardCost(self, game, player, card):
        if not hasattr(self, '_action'):
            return 0
        return self._action.hook_cardCost(game, player, card)

    def hook_cleanup(self, game, player):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_cleanup(game, player)

    def hook_gain_card(self, game, player, card):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_gain_card(game, player, card)

    def hook_postAction(self, game, player, card):
        if not hasattr(self, '_action'):
            return None
        if not hasattr(self._action, 'hook_postAction'):
            return None
        return self._action.hook_postAction(game, player, card)

    def hook_spendValue(self, game, player, card):
        if not hasattr(self, '_action'):
            return 0
        return self._action.hook_spendValue(game, player, card)

    def hook_trash_card(self, game, player, card):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_trash_card(game, player, card)

    def hook_trashThisCard(self, game, player):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_trashThisCard(game, player)

    def hook_trashcard(self, game, player):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_trashcard(game, player)

    def hook_underAttack(self, game, player, attacker):
        if not hasattr(self, '_action'):
            return None
        return self._action.hook_underAttack(player, game, attacker)


###############################################################################
class Test_BandOfMisfits(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Band of Misfits', 'Feast', 'Bureaucrat', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Band of Misfits'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_market(self):
        """ Make the Band of Misfits be a Bureaucrat """
        self.plr.test_input = ['Bureaucrat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_deck('Silver'))

    def test_play_feast(self):
        """ Make the Band of Misfits be a Feast """
        self.plr.test_input = ['Feast', 'trash', 'moat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
