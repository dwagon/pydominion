#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_HauntedWoods(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_DURATION]
        self.base = Game.ADVENTURE
        self.desc = """Until you next turn, when any other player buys a card,
            he puts his hand on top of his deck in any order.
            At the start of your next turn: +3 Cards"""
        self.name = "Haunted Woods"
        self.cost = 5

    def duration(self, game, player):
        player.pickup_cards(3)

    def hook_all_players_buy_card(self, game, player, owner, card):
        if player == owner:
            return
        if player.has_defense(owner):
            return
        player.output("%s's Haunted Woods puts your hand onto your deck" % owner.name)
        for crd in player.hand[:]:
            player.add_card(crd, "topdeck")
            player.hand.remove(crd)
            player.output("Moving %s to deck" % crd.name)


###############################################################################
class Test_HauntedWoods(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Haunted Woods"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Haunted Woods"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_buy(self):
        """Play a Haunted Woods"""
        self.vic.set_hand("Silver", "Duchy", "Province")
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.vic.set_coins(6)
        self.vic.buy_card(self.g["Gold"])
        self.assertIsNotNone(self.vic.in_deck("Silver"))
        self.assertIsNotNone(self.vic.in_deck("Duchy"))
        self.assertIsNotNone(self.vic.in_deck("Province"))
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
