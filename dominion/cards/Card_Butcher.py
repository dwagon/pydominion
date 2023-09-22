#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Butcher(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = """Take 2 coffers. You may trash a card from your hand and then pay any number of coffer.
        If you did trash a card, gain a card with a cost of up to the the cost of the trashed cards plus the number of coffers you paid"""
        self.name = "Butcher"
        self.cost = 5

    def special(self, game, player):
        player.coffers.add(2)
        trash = player.plr_choose_options(
            "Trash a card to buy a card?",
            ("Don't trash cards", False),
            ("Trash a card", True),
        )
        if not trash:
            return
        card = player.plr_trash_card(force=True)[0]
        options = []
        for i in range(player.coffers.get() + 1):
            sel = f"{i}"
            options.append({"selector": sel, "print": f"Add {i} coins", "coins": i})
        o = player.user_input(options, "Spend extra coins?")
        cost = card.cost + o["coins"]
        player.coffers -= o["coins"]
        player.plr_gain_card(cost=cost)


###############################################################################
class Test_Butcher(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Butcher"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Butcher")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a butcher"""
        self.plr.coffers.set(0)
        self.plr.test_input = ["Don't trash"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coffers.get(), 2)

    def test_trash_gold(self):
        """Trash a gold"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.coffers.set(0)
        # Trash a card
        # Trash card 3
        # Spend 2 coin
        # Buy card 1
        self.plr.test_input = ["trash a card", "trash gold", "add 2", "get silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coffers.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Gold", self.g.trash_pile)
        for m in self.plr.messages:
            if "Province" in m:
                break
        else:  # pragma: no cover
            self.fail("Couldn't get a province for 8")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
