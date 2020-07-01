#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Courtier(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = """Reveal a card from your hand. For each type it has
        (Action, Attack, etc.), choose one: +1 Action; or +1 Buy; or +3 Coin;
        or gain a Gold. The choices must be different."""
        self.name = 'Courtier'
        self.cost = 5

    def special(self, game, player):
        cards = player.cardSel()
        if not cards:
            return
        if isinstance(cards[0].cardtype, str):
            num_types = 1
        else:
            num_types = len(cards[0].cardtype)
        chosen = []
        for _ in range(num_types):
            choices = []
            if "action" not in chosen:
                choices.append(("+1 Action", "action"))
            if "buy" not in chosen:
                choices.append(("+1 Buy", "buy"))
            if "coin" not in chosen:
                choices.append(("+3 Coin", "coin"))
            if "gold" not in chosen:
                choices.append(("Gain Gold", "gold"))
            opt = player.plrChooseOptions(
                "Select one",
                *choices
            )
            chosen.append(opt)
            if opt == 'action':
                player.addActions(1)
            if opt == 'buy':
                player.addBuys(1)
            if opt == 'coin':
                player.addCoin(3)
            if opt == 'gold':
                player.gainCard('Gold')


###############################################################################
class Test_Courtier(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Courtier', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Courtier'].remove()
        self.plr.setHand('Copper', 'Moat', 'Estate')
        self.plr.addCard(self.card, 'hand')

    def test_play_action(self):
        self.plr.test_input = ['Copper', '+1 Action']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getBuys(), 1 + 0)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertIsNone(self.plr.inDiscard('Gold'))

    def test_play_buy(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Moat', '+1 Buy', '+3 Coin']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.getBuys(), 1 + 1)
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertIsNone(self.plr.inDiscard('Gold'))

    def test_play_gold(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Estate', 'Gain Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.getBuys(), 1 + 0)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
