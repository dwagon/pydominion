#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Soldier(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_TRAVELLER]
        self.base = Game.ADVENTURE
        self.desc = """+2 Coins; +1 Coin per other Attack you have in play.
        Each other player with 4 or more cards in hand discards a card."""
        self.name = "Soldier"
        self.purchasable = False
        self.coin = 2
        self.cost = 3
        self.numcards = 5

    def special(self, game, player):
        """+2 Coins; +1 Coin per other Attack you have in play.
        Each other player with 4 or more cards in hand discards a card."""
        count = 0
        for c in player.played:
            if c == self:
                continue
            if c.isAttack():
                count += 1
        player.addCoin(count)
        player.output("Gained %d extra coins" % count)
        for plr in player.attackVictims():
            if plr.hand.size() >= 4:
                plr.output("%s's Soldier: Discard a card" % player.name)
                plr.plrDiscardCards(force=True)

    def hook_discard_this_card(self, game, player, source):
        """Replace with Hero"""
        player.replace_traveller(self, "Fugitive")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(1)


###############################################################################
class Test_Soldier(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Peasant", "Militia"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Soldier"].remove()
        self.plr.add_card(self.card, "hand")

    def test_soldier(self):
        """Play a soldier with no extra attacks"""
        self.vic.set_hand("Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)

    def test_soldier_more(self):
        """Play a soldier with no extra attacks"""
        self.vic.set_hand("Copper")
        mil = self.g["Militia"].remove()
        self.plr.add_card(mil, "played")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)

    def test_soldier_attack(self):
        """Play a soldier with more than 4 cards"""
        self.vic.set_hand("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.vic.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.vic.in_discard("Gold"))
        self.assertIsNone(self.vic.in_hand("Gold"))
        self.assertEqual(self.vic.hand.size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
