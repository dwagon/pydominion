#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/The_Swamp%27s_Gift"""
import unittest

from dominion import Boon, Card, Game, Piles, Player, NoCardException


###############################################################################
class Boon_Swamps_Gift(Boon.Boon):
    """Swamp's Gift"""

    def __init__(self) -> None:
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Gain a Will-o'-Wisp from its pile."
        self.name = "The Swamp's Gift"
        self.purchasable = False
        self.required_cards = [("Card", "Will-o'-Wisp")]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Will-o'-Wisp")
        except NoCardException:
            player.output("No more Will-o'-Wisps")


###############################################################################
class Test_Swamps_Gift(unittest.TestCase):
    """Test Swamp's Gift"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        for b in self.g.boons:
            if b.name == "The Swamp's Gift":
                self.g.boons = [b]
                break
        self.card = self.g.get_card_from_pile("Bard")

    def test_winds_gift(self) -> None:
        """Test boon"""
        self.plr.add_card(self.card, Piles.HAND)
        self.g.print_state()
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Will-o'-Wisp"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
