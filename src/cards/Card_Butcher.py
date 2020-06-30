#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Butcher(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = """Take 2 coffers. You may trash a card from your hand and then pay any number of coffer.
        If you did trash a card, gain a card with a cost of up to the the cost of the trashed cards plus the number of coffers you paid"""
        self.name = 'Butcher'
        self.cost = 5

    def special(self, game, player):
        player.gainCoffer(2)
        trash = player.plrChooseOptions(
            'Trash a card to buy a card?',
            ("Don't trash cards", False), ('Trash a card', True))
        if not trash:
            return
        card = player.plrTrashCard(force=True)[0]
        options = []
        for i in range(player.getCoffer() + 1):
            sel = '%d' % i
            options.append({'selector': sel, 'print': 'Add %d coins' % i, 'coins': i})
        o = player.userInput(options, "Spend extra coins?")
        cost = card.cost + o['coins']
        player.coffer -= o['coins']
        player.plrGainCard(cost=cost)


###############################################################################
class Test_Butcher(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Butcher'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Butcher'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a butcher"""
        self.plr.coffer = 0
        self.plr.test_input = ["Don't trash"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoffer(), 2)

    def test_trash_gold(self):
        """ Trash a gold """
        self.plr.setHand('Copper', 'Gold', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.coffer = 0
        # Trash a card
        # Trash card 3
        # Spend 2 coin
        # Buy card 1
        self.plr.test_input = ['trash a card', 'trash gold', 'add 2', 'get silver']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoffer(), 0)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertIsNotNone(self.g.inTrash('Gold'))
        for m in self.plr.messages:
            if 'Province' in m:
                break
        else:   # pragma: no cover
            self.fail("Couldn't get a province for 8")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
