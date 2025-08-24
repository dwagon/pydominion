#!/usr/bin/env python
import contextlib
import unittest
from typing import Optional

from dominion import Game, Card, Piles, Player, NoCardException


class Card_Lookout(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+1 Action; Look at the top 3 cards of your deck.
            Trash one of them. Discard one of them. Put the other one on top of
            your deck"""
        self.name = "Lookout"
        self.actions = 1
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Look at the top 3 cards of your deck. Trash one of them.
        Discard one of them. Put the other one on top of your deck
        """
        cards = []
        for _ in range(3):
            with contextlib.suppress(NoCardException):
                cards.append(player.next_card())
        cards = [_ for _ in cards if _]
        if not cards:
            player.output("No cards available")
            return
        player.output(f'Pulled {", ".join([_.name for _ in cards])} from deck')
        player.output("Trash a card, discard a card, put a card on your deck")
        if trash_card := self._trash(player, cards):
            cards.remove(trash_card)
        if discard_card := self._discard(player, cards):
            cards.remove(discard_card)
        if cards:
            player.output(f"Putting {cards[0]} on top of deck")
            player.add_card(cards[0], Piles.TOPDECK)

    def _trash(self, player: Player.Player, cards: list[Card.Card]) -> Optional[Card.Card]:
        choices = []
        for card in cards:
            choices.append((f"Trash {card}", card))
        if card := player.plr_choose_options("Select a card to trash", *choices):
            player.trash_card(card)
            return card
        return None

    def _discard(self, player: Player.Player, cards: list[Card.Card]) -> Optional[Card.Card]:
        choices = [(f"Discard {card}", card) for card in cards]
        if choice := player.plr_choose_options("Select a card to discard", *choices):
            player.discard_card(choice)
            return choice
        return None


###############################################################################
class TestLookout(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Lookout"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.lookout = self.g.get_card_from_pile("Lookout")

    def test_actions(self) -> None:
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Gold", "Province")
        self.plr.add_card(self.lookout, Piles.HAND)
        self.plr.test_input = ["Province", "Gold"]
        self.plr.play_card(self.lookout)
        self.assertIn("Province", self.g.trash_pile)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DECK][0].name, "Copper")
        self.assertEqual(self.plr.piles[Piles.DECK][1].name, "Estate")

    def test_no_cards(self) -> None:
        """Play a lookout when there are no cards available"""
        trash_size = self.g.trash_pile.size()
        self.plr.piles[Piles.DECK].set()
        self.plr.add_card(self.lookout, Piles.HAND)
        self.plr.play_card(self.lookout)
        self.assertEqual(self.g.trash_pile.size(), trash_size)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
