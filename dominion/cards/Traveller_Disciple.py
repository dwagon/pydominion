#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Disciple(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TRAVELLER]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = (
            """You may play an Action card from your hand twice. Gain a copy of it"""
        )
        self.name = "Disciple"
        self.purchasable = False
        self.numcards = 5
        self.cost = 5

    def special(self, game, player):
        """You may play an Action card from your hand twice. Gain a copy of it"""
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            player.output("No suitable actions to perform")
            return
        cards = player.card_sel(cardsrc=actions)
        if not cards:
            return
        card = cards[0]
        for i in range(1, 3):
            player.output(f"Number {i} play of {card}")
            player.play_card(card, discard=False, cost_action=False)
        player.move_card(card, Piles.PLAYED)
        if card.purchasable:
            c = player.gain_card(card.name)
            if c:
                player.output(f"Gained a {c} from Disciple")

    def hook_discard_this_card(self, game, player, source):
        """Replace with Teacher"""
        player.replace_traveller(self, "Teacher")


###############################################################################
class TestDisciple(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Peasant", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Disciple")

    def test_play_no_actions(self):
        """Play a disciple with no actions available"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)

    def test_play_actions(self):
        """Play a disciple with an action available"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Moat")
        self.plr.test_input = ["moat"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
