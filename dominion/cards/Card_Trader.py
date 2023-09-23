#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Trader"""
import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Trader(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Trash a card from your hand. Gain a number of Silvers equal to its cost in coins.
        When you would gain a card, you may reveal this from your hand. If you do, instead, gain a Silver."""
        self.name = "Trader"
        self.cost = 4

    def special(self, game, player):
        card = player.plr_trash_card(
            prompt="Trash a card from your hand. Gain a number of Silvers equal to its cost in coins."
        )
        if card:
            player.output(f"Gaining {card[0].cost} Silvers")
            for _ in range(card[0].cost):
                player.gain_card("Silver")

    def hook_gain_card(self, game, player, card):
        if card.name == "Silver":
            return {}
        silver = player.plr_choose_options(
            f"From your Trader gain {card.name} or gain a Silver instead?",
            (f"Still gain {card.name}", False),
            ("Instead gain Silver", True),
        )
        if silver:
            return {"replace": "Silver", "destination": "discard"}
        return {}


###############################################################################
class TestTrader(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Trader"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Trader")

    def test_play(self):
        """Play a trader - trashing an estate"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["estate", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for i in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(i.name, "Silver")
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Estate", self.g.trash_pile)

    def test_gain(self):
        self.plr.test_input = ["Instead"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.coins.set(6)
        self.plr.buy_card("Gold")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
