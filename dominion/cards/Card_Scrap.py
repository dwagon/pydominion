#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Scrap """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Scrap(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Trash a card from your hand.
            Choose a different thing per coin it costs: +1 Card; +1 Action; +1 Buy;
            +1 Coin; gain a Silver; gain a Horse."""
        self.name = "Scrap"
        self.cost = 3
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        trc = player.plr_trash_card(
            printcost=True, prompt="Trash a card from your hand for benefits"
        )
        if not trc:
            return
        cost = min(6, player.card_cost(trc[0]))
        if not cost:
            return
        chosen = []
        for _ in range(cost):
            choices = []
            if "card" not in chosen:
                choices.append(("+1 Card", "card"))
            if "action" not in chosen:
                choices.append(("+1 Action", "action"))
            if "buy" not in chosen:
                choices.append(("+1 Buy", "buy"))
            if "coin" not in chosen:
                choices.append(("+$1 Coin", "coin"))
            if "silver" not in chosen:
                choices.append(("Gain a Silver", "silver"))
            if "horse" not in chosen:
                choices.append(("Gain a Horse", "horse"))
            opt = player.plr_choose_options("Select one", *choices)
            if opt == "card":
                player.pickup_card()
            if opt == "action":
                player.add_actions(1)
            if opt == "buy":
                player.buys.add(1)
            if opt == "coin":
                player.coins.add(1)
            if opt == "silver":
                player.gain_card("Silver")
            if opt == "horse":
                player.gain_card("Horse")
            choices.append(opt)


###############################################################################
class Test_Scrap(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Scrap"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Scrap"].remove()

    def test_playcard_cost0(self):
        """Play a scrap and trash something worth 0"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash copper", "finish"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)

    def test_playcard_cost3(self):
        """Play a scrap and trash something worth 3"""
        self.plr.piles[Piles.HAND].set("Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.test_input = [
            "trash silver",
            "card",
            "finish",
            "action",
            "finish",
            "coin",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertIn("Silver", self.g.trash_pile)

    def test_playcard_cost6(self):
        """Play a scrap and trash something worth more than 4"""
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Copper")
        self.plr.test_input = [
            "trash province",
            "card",
            "finish",
            "action",
            "finish",
            "coin",
            "finish",
            "buy",
            "finish",
            "silver",
            "finish",
            "horse",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.g.trash_pile)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertIn("Copper", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
