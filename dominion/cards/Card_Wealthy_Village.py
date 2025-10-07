#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Wealthy_Village"""
import unittest

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_WealthyVillage(Card.Card):
    """Wealthy Village"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Card; +2 Actions; When you gain this,
        if you have at least 3 differently named Treasures in play, gain a Loot."""
        self.name = "Wealthy Village"
        self.cost = 5
        self.cards = 1
        self.actions = 2
        self.required_cards = ["Loot"]

    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        """When you gain this, if you have at least 3 differently named Treasures in play, gain a Loot."""
        treasures = set([_ for _ in player.piles[Piles.PLAYED] if _.isTreasure()])
        if len(treasures) >= 3:
            player.gain_card("Loot")
        return {}


###############################################################################
class TestWealthyVillage(unittest.TestCase):
    """Test Wealthy Village"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wealthy Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Wealthy Village")

    def test_gain_action(self) -> None:
        """Play a Wealthy Village"""
        self.plr.piles[Piles.HAND].empty()
        self.plr.add_card(self.card, Piles.HAND)
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 2 - 1)  # One action to play card

    def test_gain_card(self) -> None:
        """Gain Wealthy Village"""
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Gold")
        self.plr.gain_card("Wealthy Village")
        found = any(True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot())
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
