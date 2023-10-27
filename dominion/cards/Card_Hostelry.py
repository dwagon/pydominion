#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Hostelry """

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Hostelry(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "Hostelry"
        self.cards = 1
        self.actions = 2
        self.cost = 4
        self.required_cards = [("Card", "Horse")]

    def dynamic_description(self, player):
        if player.phase == Player.Phase.BUY:
            return "+1 Card; +2 Actions; When you gain this, you may discard any number of Treasures, revealed, to gain that many Horses."
        return "+1 Card; +2 Actions"

    def hook_gain_this_card(self, game, player):
        treas = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        if not treas:
            player.output("No suitable cards for Hostelry")
            return
        discards = player.card_sel(
            prompt="Discard number of cards to gain that number of horses",
            verbs=("Discard", "Undiscard"),
            anynum=True,
            cardsrc=treas,
        )
        for crd in discards:
            player.discard_card(crd)
            player.reveal_card(crd)
            player.gain_card("Horse")


###############################################################################
class Test_Hostelry(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hostelry"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Hostelry")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_gain(self):
        """Gain the card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.test_input = ["Copper", "Silver", "Finish"]
        self.plr.gain_card("Hostelry")
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Silver", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
