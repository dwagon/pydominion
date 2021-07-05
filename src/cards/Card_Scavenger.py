#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Scavenger(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+2 Coin. You may put your deck into your discard pile.
            Look through your discard pile and put one card from it on top of
            your deck."""
        self.name = "Scavenger"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        dumpdeck = player.plrChooseOptions(
            "Put your deck into your discard pile?",
            ("Keep it where it is", False),
            ("Put deck into discard?", True),
        )
        if dumpdeck:
            for card in player.deck[:]:
                player.addCard(card, "discard")
                player.deck.remove(card)
        if player.discardpile.size():
            cards = []
            cardnames = set()
            for c in player.discardpile:
                if c.name not in cardnames:
                    cards.append(c)
                    cardnames.add(c.name)
            card = player.cardSel(
                force=True,
                cardsrc=cards,
                prompt="Pull card from discard and add to top of your deck",
            )
            player.addCard(card[0], "topdeck")
            player.discardpile.remove(card[0])


###############################################################################
class Test_Scavenger(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Scavenger", "Moat", "Witch"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Scavenger"].remove()

    def test_play(self):
        """Play a scheme"""
        self.plr.setDeck("Province", "Moat", "Witch", "Duchy")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Put", "Moat"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.deck[-1].name, "Moat")
        self.assertIsNotNone(self.plr.in_discard("Witch"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
