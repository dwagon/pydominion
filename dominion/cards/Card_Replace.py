#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Replace(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """Trash a card from your hand. Gain a card costing up to 2 more
            than it. If the gained card is an Action or Treasure, put it onto your deck;
            if it's a Victory card, each other player gains a Curse."""
        self.name = "Replace"
        self.required_cards = ["Curse"]
        self.cost = 5

    def special(self, game, player):
        tr = player.plr_trash_card()
        if not tr:
            return
        cost = tr[0].cost
        gain = player.plr_gain_card(cost, prompt=f"Gain a card costing up to {cost}")
        if not gain:
            return
        if gain.isAction() or gain.isTreasure():
            player.add_card(gain, "topdeck")
            player.discardpile.remove(gain)
        if gain.isVictory():
            for victim in player.attack_victims():
                victim.output(f"Gained a Curse due to {player.name}'s Replace")
                victim.gain_card("Curse")


###############################################################################
class Test_Replace(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Replace", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Replace"].remove()

    def test_gain_action(self):
        self.plr.hand.set("Estate", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.deck)
        self.assertNotIn("Moat", self.plr.discardpile)

    def test_gain_victory(self):
        self.plr.hand.set(
            "Estate",
            "Silver",
        )
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Estate", "Get Estate"]
        self.plr.play_card(self.card)
        self.assertIn("Curse", self.vic.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
