#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_CaravanGuard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION, Card.TYPE_REACTION]
        self.base = Game.ADVENTURE
        self.desc = """+1 Card +1 Action. At the start of your next turn, +1 Coin.
            When another player plays an Attack card, you may play this from
            your hand. (+1 Action has no effect if it's not your turn.)"""
        self.name = "Caravan Guard"
        self.cost = 3

    def special(self, game, player):
        player.add_actions(1)
        player.pickup_cards(1)

    def duration(self, game, player):
        player.add_coins(1)

    def hook_underAttack(self, game, player, attacker):
        player.output("Under attack from %s" % attacker.name)
        player.add_actions(1)
        player.pickup_cards(1)
        player.add_card(self, Card.TYPE_DURATION)
        player.hand.remove(player.in_hand("Caravan Guard"))


###############################################################################
class Test_CaravanGuard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=2, initcards=["Caravan Guard", "Militia", "Moat"]
        )
        self.g.start_game()
        self.plr, self.attacker = self.g.player_list()
        self.card = self.g["Caravan Guard"].remove()
        self.militia = self.g["Militia"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.get_coins(), 1)

    def test_attack(self):
        self.plr.set_hand("Caravan Guard", "Moat")
        self.attacker.add_card(self.militia, "hand")
        self.attacker.play_card(self.militia)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.durationpile.size(), 1)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
