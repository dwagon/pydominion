#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Vault(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = """+2 Cards; Discard any number of cards. +1 Coin per card
            discarded. Each other player may discard 2 cards. If he does, he
            draws a card."""
        self.name = "Vault"
        self.cards = 2
        self.cost = 5

    def special(self, game, player):
        discards = player.plr_discard_cards(
            anynum=True,
            prompt="Discard any number of cards. +1 Coin per card discarded",
        )
        player.add_coins(len(discards))
        player.output("Gaining %d coins" % len(discards))
        for plr in game.player_list():
            if plr != player:
                plr.output(
                    "Due to %s's Vault you may discard two cards. If you do, draw one"
                    % player.name
                )
                plrdiscards = plr.plr_discard_cards(num=2)
                if len(plrdiscards) == 2:
                    plr.pickup_card()


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class Test_Vault(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Vault"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Vault"].remove()

    def test_play(self):
        self.other.set_hand("Copper", "Silver", "Gold")
        self.plr.set_hand("Duchy", "Province", "Gold", "Silver", "Estate")
        self.plr.add_card(self.card, "hand")
        self.other.test_input = ["Copper", "Silver", "Finish"]
        self.plr.test_input = ["Duchy", "Province", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2 - 2)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.other.hand.size(), 3 - 2 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
