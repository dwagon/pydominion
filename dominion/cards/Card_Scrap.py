#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Scrap """

import unittest
from dominion import Game, Card


###############################################################################
class Card_Scrap(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
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
                player.add_buys(1)
            if opt == "coin":
                player.add_coins(1)
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
        self.plr.set_hand("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["trash copper", "finish"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Copper"))

    def test_playcard_cost3(self):
        """Play a scrap and trash something worth 3"""
        self.plr.set_hand("Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.set_deck("Province")
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
        self.assertIn("Province", self.plr.hand)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertIsNotNone(self.g.in_trash("Silver"))

    def test_playcard_cost6(self):
        """Play a scrap and trash something worth more than 4"""
        self.plr.set_hand("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.set_deck("Copper")
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
        self.assertIsNotNone(self.g.in_trash("Province"))
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertIn("Copper", self.plr.hand)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertIn("Horse", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
