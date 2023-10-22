#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Corsair"""

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Corsair(Card.Card):
    """Corsair"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+$2; At the start of your next turn, +1 Card. 
        Until then, each other player trashes the first Silver or Gold they play each turn."""
        self.coin = 2
        self.name = "Corsair"
        self.cost = 5
        self._states = {}

    def duration(self, game, player):
        """+1 Card; each other player trashes the first Silver or Gold they play each turn."""
        player.pickup_card()
        self._states = {}

    def hook_all_players_post_play(self, game, player, owner, card):
        if player == owner or owner.has_defense(player):
            return
        if card.name not in ("Gold", "Silver"):
            return
        if player.name not in self._states:
            player.trash_card(card)
            self._states[player.name] = True
            player.output(f"{owner.name}'s Corsiar trashed your {card}")
            owner.output(f"Your corsair trashed {player.name}'s {card}")


###############################################################################
class TestCorsair(unittest.TestCase):
    """Test Corsair"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Corsair"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Corsair")

    def test_play(self):
        """Play Corsair"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 1)

    def test_trash(self):
        """Test other players playing treasure"""
        self.plr.add_card(self.card, Piles.DURATION)
        self.plr.end_turn()
        # Ensure non Ag/Au cards aren't trashed
        copper = self.g.get_card_from_pile("Copper")
        self.victim.add_card(copper, Piles.HAND)
        self.victim.play_card(copper)
        self.assertNotIn("Copper", self.g.trash_pile)

        gold = self.g.get_card_from_pile("Gold")
        self.victim.add_card(gold, Piles.HAND)
        coins = self.victim.coins.get()
        self.victim.play_card(gold)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertEqual(self.victim.coins.get(), coins + 3)
        # Ensure second card isn't trashed
        silver = self.g.get_card_from_pile("Silver")
        self.victim.add_card(silver, Piles.HAND)
        self.victim.play_card(silver)
        self.assertEqual(self.victim.coins.get(), coins + 3 + 2)
        self.assertNotIn("Silver", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF