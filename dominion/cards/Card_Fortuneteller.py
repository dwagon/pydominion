#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Fortuneteller(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.CORNUCOPIA
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
                    plr.output(
                        "%s's Fortune Teller put %s on top of your deck"
                        % (player.name, card.name)
                    )
                    break
                plr.output(
                    "%s's Fortune Teller discarded your %s" % (player.name, card.name)
                )
                plr.discard_card(card)


###############################################################################
class Test_Fortuneteller(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Fortune Teller"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Fortune Teller"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Fortune Teller"""
        self.vic.set_deck("Duchy", "Silver", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIn("Silver", self.vic.discardpile)
        self.assertIn("Copper", self.vic.discardpile)
        self.assertEqual(self.vic.deck[-1].name, "Duchy")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
