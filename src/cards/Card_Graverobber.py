#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Graverobber(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """Choose one: Gain a card from the trash costing from 3 to 6,
        putting it on top of your deck; or trash an Action card from your hand and gain a card costing up to 3 more than it."""
        self.name = 'Graverobber'
        self.cost = 5

    def special(self, game, player):
        trash = player.plrChooseOptions(
            "Pick one",
            ("Gain a card from the trash costing from 3 to 6 putting it on top of your deck", False),
            ("Trash an Action card from your hand and gain a card costing up to 3 more", True))
        if trash:
            actions = [c for c in player.hand if c.isAction()]
            if not actions:
                player.output("No suitable action cards")
                return
            card = player.plrTrashCard(cardsrc=actions)
            player.plrGainCard(cost=card[0].cost+3)
        else:
            trash_cards = [c for c in game.trashpile if (3 <= c.cost <= 6)]
            if not trash_cards:
                player.output("No suitable cards in trash")
                return
            cards = player.cardSel(cardsrc=trash_cards)
            if cards:
                card = cards[0]
                game.trashpile.remove(card)
                player.addCard(card, 'topdeck')


###############################################################################
class Test_Graverobber(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Graverobber', 'Militia'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Graverobber'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_trash(self):
        """ Play a grave robber - trash a militia and gain a gold """
        militia = self.g['Militia'].remove()
        self.plr.addCard(militia, 'hand')
        self.plr.test_input = ['1', 'militia', 'gold']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNone(self.plr.inHand('Militia'))

    def test_loot(self):
        """ Play a grave robber - looting the trash """
        self.g.setTrash('Militia')
        self.plr.test_input = ['0', 'militia']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), 0)
        self.assertIsNotNone(self.plr.inDeck('Militia'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
