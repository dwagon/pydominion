#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Treasury(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = """+1 Card +1 Action +1 Coin; When you discard this from play,
            if you didn't buy a Victory card this turn, you may put this on top
            of your deck."""
        self.name = "Treasury"
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.coin = 1

    def hook_discard_this_card(self, game, player, source):
        vict = False
        for card in player.stats["bought"]:
            if card.isVictory():
                vict = True
        if vict:
            topdeck = player.plrChooseOptions(
                "Put Treasury back on top of your deck?",
                ("Discard as normal", False),
                ("Put on top of your deck", True),
            )
            if topdeck:
                player.add_card(self, "topdeck")
                player.discardpile.remove(self)


###############################################################################
class Test_Treasury(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Treasury"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Treasury"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a trader - trashing an estate"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_buy_topdeck(self):
        self.plr.test_input = ["put on top"]
        self.plr.setCoin(5)
        self.plr.buyCard(self.g["Duchy"])
        self.plr.discardCard(self.card)
        self.assertEqual(self.plr.deck[-1].name, "Treasury")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
