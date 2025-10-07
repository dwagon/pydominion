#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Lackeys"""
import unittest

from dominion import Card, Game, Piles, Player, OptionKeys, Phase


###############################################################################
class Card_Lackeys(Card.Card):
    """Lackeys"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Lackeys"
        self.cards = 2
        self.cost = 2

    ###########################################################################
    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return "+2 Cards; When you gain this, +2 Villagers."
        return "+2 Cards"

    ###########################################################################
    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        player.villagers.add(2)
        return {}


###############################################################################
class TestLackeys(unittest.TestCase):
    """Test Lackeys"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Lackeys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self) -> None:
        """Play Lackeys"""
        card = self.g.get_card_from_pile("Lackeys")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertLessEqual(self.plr.villagers.get(), 0)

    def test_gain_card(self) -> None:
        """Gain Lackeys"""
        self.plr.gain_card("Lackeys")
        self.assertLessEqual(self.plr.villagers.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
