#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Legionary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.EMPIRES
        self.desc = """+3 Coin. You may reveal a Gold from your hand.
            If you do, each other player discards down to 2 cards in hand, then draws a card."""
        self.name = "Legionary"
        self.cost = 5
        self.coin = 3

    def special(self, game, player):
        au = player.in_hand("Gold")
        if au:
            player.reveal_card(au)
            for plr in player.attack_victims():
                plr.output(
                    "%s's Legionary forces you to discard down to 2" % player.name
                )
                plr.plr_discard_down_to(2)
                plr.pickup_card()


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 2
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Legionary(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Legionary"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Legionary"].remove()

    def test_play(self):
        """Play a Legionary"""
        self.plr.set_hand("Gold")
        self.victim.test_input = ["1", "2", "3", "0"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)
        self.assertEqual(self.victim.hand.size(), 3)
        self.assertEqual(self.victim.discardpile.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
