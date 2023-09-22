#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Alchemist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "+2 cards, +1 action; When you discard this you may put on top of your deck if you have a Potion in play"
        self.name = "Alchemist"
        self.cards = 2
        self.actions = 1
        self.cost = 3
        self.potcost = True
        self.required_cards = ["Potion"]

    def hook_discard_this_card(self, game, player, source):
        """When you discard this from play, you may put this on
        top of your deck if you have a Potion in play"""
        # As we can't guarantee where we are in the discard cycle
        # We have to check the discard pile as well
        if source != "played":
            return
        if (
            "Potion" not in player.piles[Piles.PLAYED]
            and "Potion" not in player.piles[Piles.DISCARD]
        ):
            return
        ans = player.plr_choose_options(
            "What to do with the alchemist?",
            ("Discard alchemist", False),
            ("Put on top of deck", True),
        )
        if ans:
            player.move_card(self, "topdeck")


###############################################################################
class Test_Alchemist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Alchemist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.alchemist = self.g.get_card_from_pile("Alchemist")
        self.plr.add_card(self.alchemist, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.alchemist)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)

    def test_nopotion(self):
        """Discard Alchemist with no potion in play"""
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertEqual(
            self.plr.piles[Piles.DISCARD].size(), 8
        )  # 5 for hand, +2 cards, alch

    def test_discard(self):
        """Discard an Alchemist even if we have a potion in play"""
        self.plr.piles[Piles.PLAYED].set("Potion")
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertEqual(
            self.plr.piles[Piles.DISCARD].size(), 9
        )  # 5 for hand, +2 cards, alch, pot
        self.assertIn("Alchemist", self.plr.piles[Piles.DISCARD])

    def test_keep(self):
        """Keep an Alchemist for next turn"""
        self.plr.piles[Piles.PLAYED].set("Potion")
        self.plr.test_input = ["top of deck"]
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertNotIn("Alchemist", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Alchemist")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
