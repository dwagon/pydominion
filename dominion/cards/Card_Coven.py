#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Coven """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Coven(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+1 Action; +2 Coin; Each other player Exiles a Curse
            from the Supply. If they can't, they discard their Exiled Curses."""
        self.name = "Coven"
        self.actions = 1
        self.coin = 2
        self.cost = 5
        self.required_cards = ["Curse"]

    def special(self, game, player):
        for plr in player.attack_victims():
            plr.exile_card("Curse")
            if game["Curse"].is_empty():
                num = plr.unexile("Curse")
                plr.output(f"Unexiled {num} Curses from {player.name}'s Coven")
            else:
                plr.output(f"Exiled a Curse from {player.name}'s Coven")


###############################################################################
class Test_Coven(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Coven", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Coven"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Curse", self.vic.exilepile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
