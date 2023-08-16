#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea
from dominion import Game, Piles


###############################################################################
class Card_Island(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.VICTORY]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = (
            """Set aside this and another card from your hand. Return them to your deck at the end of the game.  2VP"""
        )
        self.name = "Island"
        self.cost = 4
        self.victory = 2

    def special(self, game, player):
        if not hasattr(player, "island_reserve"):
            player.island_reserve = PlayArea.PlayArea([])
        c = player.card_sel(prompt="Select a card to set aside for the rest of the game")
        if c:
            card = c[0]
            player.island_reserve.add(card)
            player.end_of_game_cards.append(card)
            player.piles[Piles.HAND].remove(card)
            player.secret_count += 1
        player.piles[Piles.PLAYED].remove(self)
        player.end_of_game_cards.append(self)
        player.island_reserve.add(self)
        player.secret_count += 1

    def hook_end_of_game(self, game, player):
        for card in player.island_reserve:
            player.output("Returning %s from Island" % card.name)
            player.add_card(card)
            player.island_reserve.remove(card)


###############################################################################
class Test_Island(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Island"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Island"].remove()

    def test_play_province(self):
        """Play an island on a province"""
        self.plr.piles[Piles.HAND].set("Silver", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["province"]
        self.plr.play_card(self.card)
        self.assertNotIn("Island", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Island", self.plr.piles[Piles.HAND])
        self.assertNotIn("Island", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])
        self.assertNotIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.secret_count, 2)
        self.plr.game_over()
        self.assertIn("Island", self.plr.piles[Piles.DISCARD])
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        score = self.plr.get_score_details()
        self.assertEqual(score["Island"], 2)
        self.assertEqual(score["Province"], 6)

    def test_play_alone(self):
        """Play a island but don't pick another card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Island", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Island", self.plr.piles[Piles.HAND])
        self.assertNotIn("Island", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.secret_count, 1)
        self.plr.game_over()
        self.assertIn("Island", self.plr.piles[Piles.DISCARD])
        score = self.plr.get_score_details()
        self.assertEqual(score["Island"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
