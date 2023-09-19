#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Giant"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Giant(Card.Card):
    """Giant"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """ Turn your Journey token over (it starts face up). If it's face
            down, +1 Coin. If it's face up, +5 Coin, and each other player
            reveals the top card of his deck, trashes it if it costs
            from 3 to 6, and otherwise discards it and gains a Curse """
        self.name = "Giant"
        self.required_cards = ["Curse"]
        self.cost = 5

    def special(self, game, player):
        if player.flip_journey_token():
            player.coins.add(5)
            for victim in player.attack_victims():
                card = victim.top_card()
                if not card:
                    continue
                victim.reveal_card(card)
                if 3 <= card.cost <= 6:
                    victim.trash_card(card)
                    victim.output(f"{player.name}'s Giant trashed your {card.name}")
                    player.output(f"Trashed {victim.name}'s {card.name}")
                else:
                    victim.output(
                        f"{player.name}'s Giant discarded your {card.name} and cursed you"
                    )
                    victim.discard_card(card)
                    victim.gain_card("Curse")
        else:
            player.coins.add(1)


###############################################################################
class TestGiant(unittest.TestCase):
    """Test Giant"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Giant"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Giant"].remove()

    def test_play_journey_trashed(self):
        """Play a giant - good journey - trashable victim"""
        self.plr.piles[Piles.HAND].set()
        self.victim.piles[Piles.DECK].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.journey_token = False
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertIn("Gold", self.g.trash_pile)

    def test_play_journey_untrashed(self):
        """Play a giant - good journey - untrashable victim"""
        self.plr.piles[Piles.HAND].set()
        self.victim.piles[Piles.DECK].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.journey_token = False
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertNotIn("Copper", self.g.trash_pile)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])

    def test_play_no_journey(self):
        """Play a giant - bad journey"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.journey_token = True
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
