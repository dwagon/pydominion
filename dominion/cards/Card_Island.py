#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import PlayArea, Player
from dominion import Game, Piles


###############################################################################
class Card_Island(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.VICTORY]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = (
            """Set aside this and another card from your hand. Return them to your deck at the end of the game. 2VP"""
        )
        self.name = "Island"
        self.cost = 4
        self.victory = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if not hasattr(player, "_island_reserve"):
            player._island_reserve = PlayArea.PlayArea(initial=[])
        if c := player.card_sel(prompt="Select a card to set aside for the rest of the game"):
            card = c[0]
            player._island_reserve.add(card)
            player.end_of_game_cards.append(card)
            player.piles[Piles.HAND].remove(card)
            player.secret_count += 1
        if self in player.piles[Piles.PLAYED]:  # If Island is not played from hand
            player.piles[Piles.PLAYED].remove(self)
            player.end_of_game_cards.append(self)
            player._island_reserve.add(self)
            player.secret_count += 1

    def hook_end_of_game(self, game: Game.Game, player: Player.Player) -> None:
        for card in player._island_reserve:
            player.output(f"Returning {card} from Island")
            player.add_card(card)
            player._island_reserve.remove(card)

    def debug_dump(self, player: Player.Player) -> None:
        print(f"Island Reserve: {self}: {self.player._island_reserve}")


###############################################################################
class Test_Island(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Island"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Island")

    def test_play_province(self) -> None:
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

    def test_play_alone(self) -> None:
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
