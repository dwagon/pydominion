#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Teacher(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RESERVE]
        self.base = Game.ADVENTURE
        self.desc = """At the start of your turn, you may call this,
            to move your +1 Card, +1 Action, +1 Buy or +1 Coin token
            to an Action Supply pile you have no tokens on"""
        self.name = 'Teacher'
        self.purchasable = False
        self.cost = 6
        self.numcards = 5

    def special(self, game, player):
        """At the start of your turn, you may call this, to move your +1 Card,
        +1 Action, +1 Buy or +1 Coin token to an Action Supply pile you have
        no tokens on"""
        for tkn in ('+1 Card', '+1 Action', '+1 Buy', '+1 Coin'):
            actionpiles = self.which_stacks(game, player)
            prompt = 'Which stack do you want to add the %s token to?' % tkn
            if player.tokens[tkn]:
                prompt += ' Currently on %s' % player.tokens[tkn]
            stacks = player.cardSel(num=1, prompt=prompt, cardsrc=actionpiles)
            if stacks:
                player.place_token(tkn, stacks[0].name)

    def which_stacks(self, game, player):
        return [ap for ap in game.getActionPiles() if not player.which_token(ap.name)]


###############################################################################
class Test_Teacher(unittest.TestCase):
    def setUp(self):
        initcards = ['Page', 'Cellar', 'Chapel', 'Moat', 'Vassal', 'Village', 'Harbinger', 'Workshop', 'Bureaucrat', 'Venture']
        self.g = Game.Game(quiet=True, numplayers=1, initcards=initcards)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Teacher'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.test_input = ['Cellar', 'Chapel', 'Moat', 'Vassal']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.tokens['+1 Card'], 'Cellar')
        self.assertEqual(self.plr.tokens['+1 Action'], 'Chapel')
        self.assertEqual(self.plr.tokens['+1 Buy'], 'Moat')
        self.assertEqual(self.plr.tokens['+1 Coin'], 'Vassal')

    def test_which_stacks(self):
        output = self.card.which_stacks(self.g, self.plr)
        self.assertEqual(len(output), 9)
        for c in output:
            if c.name == 'Venture':
                self.fail("Non action card in action card list")
        self.plr.place_token('+1 Card', 'Moat')
        output = self.card.which_stacks(self.g, self.plr)
        self.assertEqual(len(output), 8)
        for c in output:
            if c.name == 'Moat':
                self.fail("Card with token in action card list")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
