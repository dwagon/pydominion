#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Phase


###############################################################################
class Card_Raider(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.NIGHT,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Each other player with 5 or more cards in hand discards
            a copy of a card you have in play (or reveals they can't). At the
            start of your next turn, +3 Coins"""
        self.name = "Raider"
        self.cost = 6

    def duration(self, game, player):
        player.coins.add(3)

    def night(self, game, player):
        inplay = {_.name for _ in player.piles[Piles.PLAYED]}
        for pl in player.attack_victims():
            if pl.piles[Piles.HAND].size() >= 5:
                player.output(f"Raiding {pl.name}")
                todiscard = []
                for c in pl.piles[Piles.HAND]:
                    if c.name in inplay:
                        pl.output(f"{player.name}'s Raider discarded your {c.name}")
                        player.output(f"Raider discarded {pl.name}'s {c.name}")
                        todiscard.append(c)
                if not todiscard:
                    for card in pl.piles[Piles.HAND]:
                        pl.reveal_card(card)
                for c in todiscard[:]:
                    pl.discard_card(c)


###############################################################################
class TestRaider(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Raider"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Raider")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a Raider"""
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.PLAYED].set("Gold", "Silver")
        self.victim.piles[Piles.HAND].set(
            "Silver", "Gold", "Estate", "Copper", "Copper"
        )
        self.plr.play_card(self.card)
        try:
            self.assertIn("Gold", self.victim.piles[Piles.DISCARD])
            self.assertIn("Silver", self.victim.piles[Piles.DISCARD])
            self.assertNotIn("Gold", self.victim.piles[Piles.HAND])
            self.assertNotIn("Silver", self.victim.piles[Piles.HAND])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise
        self.plr.end_turn()
        self.plr.start_turn()
        try:
            self.assertEqual(self.plr.coins.get(), 3)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
