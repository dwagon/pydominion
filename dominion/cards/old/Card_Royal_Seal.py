#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, OptionKeys


###############################################################################
class Card_RoyalSeal(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+2 Coin. While this is in play, when you gain a card, you may put that card on top of your deck."
        self.playable = False
        self.name = "Royal Seal"
        self.cost = 5
        self.coin = 2

    def hook_gain_card(self, game, player, card):
        """While this is in play, when you gain a card, you may put that card on top of your deck"""
        mod = {}
        deck = player.plr_choose_options(
            f"Where to put {card}?",
            (f"Put {card} on discard", False),
            (f"Put {card} on top of deck", True),
        )
        if deck:
            player.output(f"Putting {card} on deck due to Royal Seal")
            mod[OptionKeys.DESTINATION] = Piles.TOPDECK
        return mod


###############################################################################
class TestRoyalSeal(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Royal Seal"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Royal Seal")

    def test_play(self):
        """Play a Royal Seal"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_discard(self):
        """Have a Royal Seal  - discard the gained card"""
        self.plr.piles[Piles.PLAYED].set("Royal Seal")
        self.plr.test_input = ["discard"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])

    def test_deck(self):
        """Have a Royal Seal  - the gained card on the deck"""
        self.plr.piles[Piles.PLAYED].set("Royal Seal")
        self.plr.test_input = ["deck"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
