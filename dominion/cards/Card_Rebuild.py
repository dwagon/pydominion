#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Rebuild(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 action. Name a card. Reveal cards from the top
        of your deck until you reveal a Victory card that is
        not the named card.  Discard the other cards.
        Trash the Victory card and gain a Victory card cost up to 3 more than it"""
        self.name = "Rebuild"
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """Name a card. Reveal cards from the top of your deck
        until you reveal a Victory card that is not the named card.
        Discard the other cards. Trash the Victory card and gain a
        Victory card cost up to 3 more than it"""
        stacks = game.getVictoryPiles()
        cards = player.card_sel(
            prompt="Guess a victory card - the next victory card that is not that will be upgraded",
            cardsrc=stacks,
        )
        if cards:
            guess = cards[0]
        else:
            return
        discards = []
        while True:
            card = player.next_card()
            player.reveal_card(card)
            if not card:
                break
            if card.isVictory() and guess.name != card.name:
                player.output("Found and trashing a %s" % card.name)
                player.trash_card(card)
                player.plr_gain_card(card.cost + 3, modifier="less", types={Card.CardType.VICTORY: True})
                break
            player.output("Drew and discarded %s" % card.name)
            discards.append(card)
        for c in discards:
            player.discard_card(c)


###############################################################################
class Test_Rebuild(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Rebuild"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Rebuild"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a rebuild"""
        tsize = self.g.trashpile.size()
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Estate", "Province", "Gold")
        self.plr.test_input = ["Select Province", "Get Duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.g.trashpile.size(), tsize + 1)
        self.assertIn("Estate", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
