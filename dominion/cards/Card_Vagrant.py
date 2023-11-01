#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Vagrant(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 card, +1 action, Reveal the top card of your deck.
            If it's a Curse, Ruins, Shelter or Victory card, put it into your hand"""
        self.name = "Vagrant"
        self.actions = 1
        self.cards = 1
        self.cost = 2

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Reveal the top card of your deck. If it's a Curse,
        Ruins, Shelter or Victory card, put it into your hand"""
        card = player.next_card()
        if card is None:
            return
        player.reveal_card(card)
        if (
            card.isVictory()
            or card.isRuin()
            or card.isShelter()
            or card.name == "Ruins"
        ):
            player.add_card(card, Piles.HAND)
            player.output(f"Adding {card} to hand")
        else:
            player.add_card(card, "topdeck")
            player.output(f"Top card {card} still on deck")


###############################################################################
class Test_Vagrant(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Vagrant"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Vagrant")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play the vagrant with unexciting next card"""
        self.plr.piles[Piles.DECK].set("Gold", "Silver", "Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        card = self.plr.next_card()
        assert card is not None
        self.assertEqual(card.name, "Silver")

    def test_play_exciting(self) -> None:
        """Play the vagrant with an exciting next card"""
        self.plr.piles[Piles.DECK].set("Estate", "Province", "Duchy")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertIn("Province", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
