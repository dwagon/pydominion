#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Goons(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = "Other players discard down to 3. +1 VP when buying"
        self.name = "Goons"
        self.cost = 6
        self.buys = 1
        self.coin = 2

    def special(self, game, player):
        """Each other player discards down to three cards"""
        for plr in player.attack_victims():
            plr.output("Discard down to 3 cards")
            plr.plr_discard_down_to(3)

    def hook_buy_card(self, game, player, card):
        """While this card is in play, when you buy a card +1 VP"""
        player.output("Scored 1 more from goons")
        player.add_score("Goons", 1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Goons(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Goons", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Goons"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.victim.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.victim.hand.size(), 3)

    def test_defended(self):
        self.victim.hand.set("Moat", "Estate", "Gold", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.victim.hand.size(), 4)

    def test_buy(self):
        self.victim.hand.set("Moat", "Estate", "Gold", "Copper")
        self.plr.play_card(self.card)
        self.plr.buy_card(self.g["Copper"])
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Goons"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
