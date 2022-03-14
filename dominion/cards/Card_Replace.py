#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Replace(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.INTRIGUE
        self.desc = """Trash a card from your hand. Gain a card costing up to 2 more
            than it. If the gained card is an Action or Treasure, put it onto your deck;
            if it's a Victory card, each other player gains a Curse."""
        self.name = "Replace"
        self.required_cards = ["Curse"]
        self.cost = 5

    def special(self, game, player):
        tr = player.plrTrashCard()
        if not tr:
            return
        cost = tr[0].cost
        gain = player.plrGainCard(
            cost, prompt="Gain a card costing up to {}".format(cost)
        )
        if not gain:
            return
        if gain.isAction() or gain.isTreasure():
            player.add_card(gain, "topdeck")
            player.discardpile.remove(gain)
        if gain.isVictory():
            for victim in player.attackVictims():
                victim.output("Gained a Curse due to {}'s Replace".format(player))
                victim.gainCard("Curse")


###############################################################################
class Test_Replace(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Replace", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Replace"].remove()

    def test_gain_action(self):
        self.plr.set_hand("Estate", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "Get Moat"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_deck("Moat"))
        self.assertIsNone(self.plr.in_discard("Moat"))

    def test_gain_victory(self):
        self.plr.set_hand(
            "Estate",
            "Silver",
        )
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "Get Estate"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.vic.in_discard("Curse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
