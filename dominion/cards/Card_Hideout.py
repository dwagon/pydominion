#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Hideout"""
import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Hideout(Card.Card):
    """Hideout"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+1 Card; +2 Actions; Trash a card from your hand. If it's a Victory card, gain a Curse."""
        self.name = "Hideout"
        self.required_cards = ["Curse"]
        self.actions = 2
        self.cards = 1
        self.cost = 4

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        card = player.plr_trash_card(num=1, force=True)
        if card and card[0].isVictory():
            try:
                player.gain_card("Curse")
            except NoCardException:
                player.output("No more Curses")


###############################################################################
class TestHideout(unittest.TestCase):
    """Test Hideout"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Hideout"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self) -> None:
        """Play Hideout"""
        self.plr.piles[Piles.DECK].set("Silver")
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        card = self.g.get_card_from_pile("Hideout")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Trash Copper"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)

    def test_trash_victory(self) -> None:
        """Trash a victory"""
        self.plr.piles[Piles.DECK].set("Silver")
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        card = self.g.get_card_from_pile("Hideout")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Trash Estate"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertIn("Curse", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
