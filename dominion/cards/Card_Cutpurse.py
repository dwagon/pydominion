#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Cutpurse"""
import unittest

from dominion import Game, Piles, Player, Card


###############################################################################
class Card_Cutpurse(Card.Card):
    """Cutpurse"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.desc = "+2 coin; Each other player discards a Copper card (or reveals a hand with no Copper)."
        self.name = "Cutpurse"
        self.coin = 2
        self.cost = 4
        self.base = Card.CardExpansion.SEASIDE

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Each other player discard a Copper card (or reveals a
        hand with no copper)."""
        for victim in player.attack_victims():
            c = victim.piles[Piles.HAND]["Copper"]
            if c:
                player.output(f"{victim} discarded a copper")
                victim.output(f"Discarded a copper due to {player}'s Cutpurse")
                victim.discard_card(c)
            else:
                for card in victim.piles[Piles.HAND]:
                    victim.reveal_card(card)
                player.output(f"{victim} had no coppers")


###############################################################################
class TestCutpurse(unittest.TestCase):
    """Test Cutpurse"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Cutpurse"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Cutpurse")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_coppers(self):
        self.victim.piles[Piles.HAND].set("Copper", "Copper", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.victim.piles[Piles.DISCARD][-1].name, "Copper")
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 2)

    def test_play_none(self):
        self.victim.piles[Piles.HAND].set("Duchy", "Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
