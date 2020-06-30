#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Embargo(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = """+2 Coin. Trash this card. Put an Embargo token on top of a Supply pile.
        When a player buys a card, he gains a Curse card per Embargo token on that pile."""
        self.name = 'Embargo'
        self.required_cards = ['Curse']
        self.coin = 2
        self.cost = 2

    def special(self, game, player):
        trash = player.plrChooseOptions(
            "Trash this card?",
            ("Keep this card", False),
            ("Trash this card to embargo", True))
        if not trash:
            return
        player.trashCard(self)
        piles = [cp for cp in game.cardpiles.values()]
        piles.sort()
        card = player.cardSel(
            cardsrc=piles,
            prompt="Which stack to embargo"
            )
        game[card[0].name].embargo()


###############################################################################
class Test_Embargo(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Embargo'])
        self.g.start_game()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['Embargo'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['trash', 'Select Silver']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.g['Silver'].embargo_level, 1)
        self.assertIsNotNone(self.g.inTrash('Embargo'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
