#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Leprechaun(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Gain a Gold. If you have exactly 7 cards in play, gain a Wish from its pile.
            Otherwise, receive a Hex."""
        self.name = "Leprechaun"
        self.required_cards = [("Card", "Wish")]
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Gold")
        except NoCardException:  # pragma: no cover
            player.output("No more Gold")
        if player.piles[Piles.PLAYED].size() + player.piles[Piles.DURATION].size() == 7:
            try:
                player.gain_card("Wish")
            except NoCardException:  # pragma: no cover
                player.output("No more Wishes")
        else:
            player.receive_hex()


###############################################################################
class TestLeprechaun(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Leprechaun", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Leprechaun")
        self.plr.add_card(self.card, Piles.HAND)
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_with_not_seven(self) -> None:
        """Play a Leprechaun with not 7 cards"""
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertTrue(self.plr.has_state("Deluded"))

    def test_play_with_seven(self) -> None:
        """Play a Leprechaun with 7 cards in play"""
        self.plr.piles[Piles.PLAYED].set("Moat", "Moat", "Moat", "Moat", "Moat", "Moat")  # + Leprec
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertFalse(self.plr.has_state("Deluded"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
