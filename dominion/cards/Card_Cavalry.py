#!/usr/bin/env python

import unittest
from dominion import Card, Player, Game, Piles


###############################################################################
class Card_Cavalry(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "Cavalry"
        self.cost = 4
        self.required_cards = [("Card", "Horse")]

    def dynamic_description(self, player):
        if player.phase == Player.Phase.ACTION:
            return "Gain 2 Horses."
        return """Gain 2 Horses. When you gain this, +2 Cards, +1 Buy,
            and if it's your Buy phase return to your Action phase."""

    def special(self, game, player):
        player.gain_card("Horse")
        player.gain_card("Horse")

    def hook_gain_this_card(self, game, player):
        if player.phase == Player.Phase.BUY:
            player.phase = Player.Phase.ACTION
        player.pickup_cards(2)
        player.buys.add(1)


###############################################################################
class TestCavalry(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Cavalry"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Cavalry")

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])

    def test_gain(self):
        self.plr.phase = Player.Phase.BUY
        self.plr.gain_card("Cavalry")
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 1 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertEqual(self.plr.phase, Player.Phase.ACTION)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
