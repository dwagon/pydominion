#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Specialist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.name = "Specialist"
        self.desc = (
            "You may play an Action or Treasure from your hand. Choose one: play it again; or gain a copy of it."
        )
        self.cost = 5

    def special(self, game, player):
        from_cards = [_ for _ in player.piles[Piles.HAND] if _.isAction() or _.isTreasure()]
        cards = player.card_sel(cardsrc=from_cards, prompt="Play which card?")
        chosen = cards[0]
        player.play_card(chosen, discard=False, cost_action=False)
        play_again = player.plr_choose_options(
            f"What to do with {chosen.name}?",
            ("Play it again?", True),
            ("Gain a copy of it?", False),
        )
        if play_again:
            player.play_card(chosen, discard=False, cost_action=False)
        else:
            player.gain_card(chosen.name)


###############################################################################
class Test_Specialist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Specialist", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Specialist"].remove()

    def test_play_gain(self):
        """Play the card and gain a copy"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Moat", "Gain a copy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1 + 2)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])

    def test_play_again(self):
        """Play the card and play it again"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Moat", "Play it again"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1 + 2 + 2)
        self.assertNotIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
