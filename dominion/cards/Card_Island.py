#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea
from dominion import Game


###############################################################################
class Card_Island(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_VICTORY]
        self.base = Game.SEASIDE
        self.desc = """Set aside this and another card from your hand. Return them to your deck at the end of the game.  2VP"""
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
            player.hand.remove(card)
            player.secret_count += 1
        player.played.remove(self)
        player.end_of_game_cards.append(self)
        player.island_reserve.add(self)
        player.secret_count += 1

    def hook_end_of_game(self, game, player):
        for card in player.island_reserve[:]:
            player.output("Returning %s from Island" % card.name)
            player.add_card(card)
            player.island_reserve.remove(card)


###############################################################################
class Test_Island(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Island"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Island"].remove()

    def test_play_province(self):
        """Play an island on a province"""
        self.plr.set_hand("Silver", "Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["province"]
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.in_played("Island"))
        self.assertIsNone(self.plr.in_hand("Island"))
        self.assertIsNone(self.plr.in_discard("Island"))
        self.assertIsNone(self.plr.in_hand("Province"))
        self.assertIsNone(self.plr.in_discard("Province"))
        self.assertEqual(self.plr.secret_count, 2)
        self.plr.game_over()
        self.assertIsNotNone(self.plr.in_discard("Island"))
        self.assertIsNotNone(self.plr.in_discard("Province"))
        score = self.plr.get_score_details()
        self.assertEqual(score["Island"], 2)
        self.assertEqual(score["Province"], 6)

    def test_play_alone(self):
        """Play a island but don't pick another card"""
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.in_played("Island"))
        self.assertIsNone(self.plr.in_hand("Island"))
        self.assertIsNone(self.plr.in_discard("Island"))
        self.assertEqual(self.plr.secret_count, 1)
        self.plr.game_over()
        self.assertIsNotNone(self.plr.in_discard("Island"))
        score = self.plr.get_score_details()
        self.assertEqual(score["Island"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
