#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Animal_Fair """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Animal_Fair(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+4 Coin; +1 Buy per empty supply pile.
            Instead of paying this card's cost, you may trash an Action card
            from your hand."""
        self.name = "Animal Fair"
        self.coin = 4
        self.always_buyable = True
        self.cost = 7

    def special(self, game, player):
        empties = sum(1 for st in game.card_piles if game[st].is_empty())
        player.buys.add(empties)

    def todo_hook_buy_this_card(self, game, player):
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            return 0
        tc = player.plr_trash_card(prompt="Trash card to get Animal Fair for free", cardsrc=actions)
        if tc:
            return -7
        return 0


###############################################################################
class Test_Animal_Fair(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Animal Fair", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Animal Fair"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a supplies"""
        c = self.g["Moat"].remove()
        while c:
            c = self.g["Moat"].remove()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 4)
        self.assertEqual(self.plr.buys.get(), 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
