#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Cardinal """

import unittest
from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Cardinal(Card.Card):
    """Cardinal"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Each other player reveals the top 2 cards of their deck,
            Exiles one costing from 3 to 6, and discards the rest."""
        self.name = "Cardinal"
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        for plr in player.attack_victims():
            exile_count = 0
            for _ in range(2):
                try:
                    card = plr.pickup_card()
                except NoCardException:
                    continue
                plr.reveal_card(card)
                if 3 <= card.cost <= 6 and not exile_count:
                    plr.exile_card(card)
                    plr.output(f"{player.name}'s Cardinal exiled your {card}")
                    exile_count += 1
                else:
                    plr.output(f"{player.name}'s Cardinal discarded your {card}")
                    plr.discard_card(card)


###############################################################################
class TestCardinal(unittest.TestCase):
    """Test Cardinal"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Cardinal", "Village"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("Cardinal")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Test play"""
        self.oth.piles[Piles.DECK].set("Silver", "Village")
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.oth.piles[Piles.DISCARD])
        self.assertIn("Village", self.oth.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
