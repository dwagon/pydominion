#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Landing_Party"""

import unittest

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_LandingParty(Card.Card):
    """Landing Party"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+2 Cards; +2 Actions; The next time the first card you play on a turn is a Treasure,
        put this onto your deck afterwards."""
        self.name = "Landing Party"
        self.cost = 4
        self.cards = 2
        self.actions = 2
        self.permanent = True

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        """The next time the first card you play on a turn is a Treasure,
        put this onto your deck afterwards."""
        if not card.isTreasure() or len(player.piles[Piles.PLAYED]) != 1:
            return {}
        player.output("Moving Landing Party back on deck")
        player.move_card(self, Piles.DECK)
        return {}


###############################################################################
class TestLandingParty(unittest.TestCase):
    """Test Landing Party"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Landing Party"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Landing Party")

    def test_play(self) -> None:
        """Play Card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertNotIn("Landing Party", self.plr.piles[Piles.DECK])
        copper = self.g.get_card_from_pile("Copper")
        self.plr.add_card(copper, Piles.HAND)
        self.plr.play_card(copper)
        self.assertIn("Landing Party", self.plr.piles[Piles.DECK])
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
