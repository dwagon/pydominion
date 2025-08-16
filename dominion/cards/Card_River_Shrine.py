#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/River_Shrine"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_River_Shrine(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.OMEN]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Sun; Trash up to 2 cards from your hand.
            At the start of Clean-up, if you didn't gain any cards in your Buy phase this turn,
            gain a card costing up to $4."""
        self.name = "River Shrine"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash up to 2 cards from your hand."""
        player.plr_trash_card(num=2)

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> None:
        """At the start of Clean-up, if you didn't gain any cards in your
        Buy phase this turn, gain a card costing up to $4."""
        if not player.stats["bought"]:
            player.plr_gain_card(cost=4)


###############################################################################
class Test_River_Shrine(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["River Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("River Shrine")

    def test_play(self) -> None:
        """Play card - buy nothing"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Estate", "Duchy", "River Shrine")
        self.plr.test_input = [
            "Play River Shrine",
            "Trash Copper",
            "Trash Estate",
            "Finish",
            "End Phase",  # Action Phase
            "End Phase",  # Buy Phase
            "Get Silver",
        ]
        self.plr.turn()
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_buy(self) -> None:
        """Play card - buy something"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy", "River Shrine")
        self.plr.test_input = [
            "Play River Shrine",
            "Trash Copper",
            "Trash Estate",
            "Finish",
            "End Phase",  # Action
            "Buy Copper",
            "End Phase",  # Buy
        ]
        self.plr.turn()
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
