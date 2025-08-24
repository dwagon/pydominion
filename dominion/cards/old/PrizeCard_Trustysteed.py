#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Option


###############################################################################
class Card_TrustySteed(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.PRIZE]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.name = "Trusty Steed"
        self.purchasable = False
        self.cost = 0
        self.desc = "Choose two: +2 Cards; or +2 Actions; or +2 Coin; or gain 4 Silvers and put your deck into your discard pile."

    def special(self, game, player):
        selectable = [
            ("+2 cards", "cards"),
            ("+2 actions", "actions"),
            ("+2 Coins", "coins"),
            ("4 Silvers", "silvers"),
        ]
        chosen = []
        for _ in range(2):
            options = []
            index = 1
            for p, o in selectable:
                if o in chosen:
                    continue
                options.append(Option(selector=str(index), print=p, opt=o))
                index += 1
            choice = player.user_input(options, "What do you want to do?")
            chosen.append(choice["opt"])

        for choice in chosen:
            if choice == "cards":
                player.pickup_cards(2)
            elif choice == "actions":
                player.add_actions(2)
            elif choice == "coins":
                player.coins.add(2)
            elif choice == "silvers":
                for _ in range(4):
                    player.gain_card("Silver")


###############################################################################
class TestTrustySteed(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, oldcards=True, numplayers=1, initcards=["Tournament"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Trusty Steed")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_a(self):
        self.plr.test_input = ["cards", "coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_play_b(self):
        self.plr.test_input = ["action", "silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 4)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
