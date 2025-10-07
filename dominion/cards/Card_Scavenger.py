#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Scavenger"""
import unittest

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_Scavenger(Card.Card):
    """Scavenger"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 Coin. You may put your deck into your discard pile.
            Look through your discard pile and put one card from it on top of
            your deck."""
        self.name = "Scavenger"
        self.coin = 2
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        if player.plr_choose_options(
            "Put your deck into your discard pile?",
            ("Keep it where it is", False),
            ("Put deck into discard?", True),
        ):
            for card in player.piles[Piles.DECK]:
                player.add_card(card, Piles.DISCARD)
                player.piles[Piles.DECK].remove(card)

        if player.piles[Piles.DISCARD].size():
            discard_cards = []
            card_names = set()
            for c in player.piles[Piles.DISCARD]:
                if c.name not in card_names:
                    discard_cards.append(c)
                    card_names.add(c.name)
            cards = player.card_sel(
                force=True,
                cardsrc=discard_cards,
                prompt="Pull card from discard and add to top of your deck",
            )
            player.add_card(cards[0], Piles.TOPDECK)
            player.piles[Piles.DISCARD].remove(cards[0])


###############################################################################
class TestScavenger(unittest.TestCase):
    """Test Scavenger"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Scavenger", "Moat", "Witch"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Scavenger")

    def test_play(self):
        """Play a scheme"""
        self.plr.piles[Piles.DECK].set("Province", "Moat", "Witch", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Put", "Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Moat")
        self.assertIn("Witch", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
