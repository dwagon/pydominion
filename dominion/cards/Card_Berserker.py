#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Berserker"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Berserker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Gain a card costing less than this. Each other player discards down to 3 cards in hand.
        When you gain this, if you have an Action in play, play this."""
        self.name = "Berserker"
        self.cost = 5

    def special(self, game, player):
        """Berserker Special"""
        cost = player.card_cost(self)
        player.plr_gain_card(cost - 1)
        for victim in player.attack_victims():
            victim.output(
                f"{player.name}'s Berserker causes you to discard down to 3 cards"
            )
            victim.plr_discard_down_to(3)

    def hook_gain_this_card(self, game, player):
        has_action = sum([1 for _ in player.piles[Piles.PLAYED] if _.isAction()])
        if has_action:
            player.play_card(self, cost_action=False, discard=False)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    num_to_discard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(num_to_discard)


###############################################################################
class Test_Berserker(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Berserker"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Berserker")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a Berserker"""
        self.plr.test_input = ["Get Silver"]
        self.victim.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_gain_no_action(self):
        """Gain a berserker with no action in play"""
        self.plr.gain_card("Berserker")
        self.assertIn("Berserker", self.plr.piles[Piles.DISCARD])

    def test_gain_with_action(self):
        """Gain a berserker with no action in play"""
        self.plr.piles[Piles.PLAYED].set("Berserker")
        self.plr.test_input = ["Get Silver"]
        self.victim.test_input = ["1", "2", "0"]
        self.plr.gain_card("Berserker")
        self.assertIn("Berserker", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
