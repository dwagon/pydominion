#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Courtier(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = """Reveal a card from your hand. For each type it has
        (Action, Attack, etc.), choose one: +1 Action; or +1 Buy; or +3 Coin;
        or gain a Gold. The choices must be different."""
        self.name = "Courtier"
        self.cost = 5

    def special(self, game, player):
        cards = player.card_sel()
        if not cards:
            return
        if isinstance(cards[0].cardtype, str):
            num_types = 1
        else:
            num_types = len(cards[0].cardtype)
        chosen = []
        for _ in range(num_types):
            choices = []
            if "action" not in chosen:
                choices.append(("+1 Action", "action"))
            if "buy" not in chosen:
                choices.append(("+1 Buy", "buy"))
            if "coin" not in chosen:
                choices.append(("+3 Coin", "coin"))
            if "gold" not in chosen:
                choices.append(("Gain Gold", "gold"))
            opt = player.plr_choose_options("Select one", *choices)
            chosen.append(opt)
            if opt == Card.TYPE_ACTION:
                player.add_actions(1)
            if opt == "buy":
                player.add_buys(1)
            if opt == "coin":
                player.add_coins(3)
            if opt == "gold":
                player.gain_card("Gold")


###############################################################################
class Test_Courtier(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Courtier", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Courtier"].remove()
        self.plr.set_hand("Copper", "Moat", "Estate")
        self.plr.add_card(self.card, "hand")

    def test_play_action(self):
        self.plr.test_input = ["Copper", "+1 Action"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 1 + 0)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertIsNone(self.plr.in_discard("Gold"))

    def test_play_buy(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Moat", "+1 Buy", "+3 Coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.get_buys(), 1 + 1)
        self.assertEqual(self.plr.get_coins(), 3)
        self.assertIsNone(self.plr.in_discard("Gold"))

    def test_play_gold(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Estate", "Gain Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.get_buys(), 1 + 0)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertIsNotNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
