#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Fortuneteller(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """2 Coin. Each other player reveals cards from the top of his deck
        until he reveals a Victory or Curse card. He puts it on top and discards the other revealed cards."""
        self.name = "Fortune Teller"
        self.coin = 2
        self.cost = 3

    def special(self, game, player):
        for plr in player.attack_victims():
            while True:
                card = plr.next_card()
                plr.reveal_card(card)
                if not card:
                    break
                if card.isVictory() or card.name == "Curse":
                    plr.add_card(card, "topdeck")
                    plr.output("%s's Fortune Teller put %s on top of your deck" % (player.name, card.name))
                    break
                plr.output("%s's Fortune Teller discarded your %s" % (player.name, card.name))
                plr.discard_card(card)


###############################################################################
class Test_Fortuneteller(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Fortune Teller"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Fortune Teller")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Fortune Teller"""
        self.vic.piles[Piles.DECK].set("Duchy", "Silver", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Silver", self.vic.piles[Piles.DISCARD])
        self.assertIn("Copper", self.vic.piles[Piles.DISCARD])
        self.assertEqual(self.vic.piles[Piles.DECK][-1].name, "Duchy")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
