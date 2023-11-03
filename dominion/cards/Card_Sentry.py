#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sentry """

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Sentry(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = """+1 Card; +1 Action; Look at the top 2 cards of your deck.
            Trash and/or discard any number of them. Put the rest back on top
            in any order."""
        self.name = "Sentry"
        self.cost = 5
        self.cards = 1
        self.actions = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        cards: list[Card.Card] = []
        for _ in range(2):
            try:
                cards.append(player.next_card())
            except NoCardException:
                continue
        player.output(
            "Look at the top two cards of your deck. Trash, discard or move to deck"
        )
        player.output(f"Trash any/all of {self.names(cards)}")
        to_trash = player.plr_trash_card(cardsrc=cards, num=2)
        cards = [_ for _ in cards if _ and _ not in to_trash]
        if not cards:
            return
        player.output(f"Discard any/all of {self.names(cards)}")
        to_discard = player.plr_discard_cards(cardsrc=cards, num=2)
        if to_deck := [
            player.add_card(_, Piles.DECK) for _ in cards if _ not in to_discard
        ]:
            player.output(f"Moving {self.names(to_deck)} to the deck")

    def names(self, cards: list[Card.Card]) -> str:
        return ", ".join([_.name for _ in cards if _ is not None])


###############################################################################
class TestSentry(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sentry"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sentry")
        self.plr.add_card(self.card, Piles.HAND)

    def test_trash_discard(self) -> None:
        self.plr.piles[Piles.DECK].set("Copper", "Province", "Duchy")
        self.plr.test_input = ["Trash Copper", "Finish", "Discard Province", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])

    def test_discard_keep(self) -> None:
        self.plr.piles[Piles.DECK].set("Gold", "Province", "Duchy")
        self.plr.test_input = ["Finish", "Discard Province", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
