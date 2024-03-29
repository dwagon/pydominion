#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Miller(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TOWNSFOLK]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.actions = 1
        self.name = "Miller"
        self.desc = """+1 Action; Look at the top 4 cards of your deck. Put one into your hand and discard the rest."""
        self.pile = "Townsfolk"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        cards: list[Card.Card] = []
        for _ in range(4):
            try:
                card = player.next_card()
            except NoCardException:  # pragma: no coverage
                break
            cards.append(card)
        if ch := player.card_sel(
            prompt="Pick a card to put into your hand", cardsrc=cards
        ):
            player.add_card(ch[0], Piles.HAND)
            cards.remove(ch[0])
        for card in cards:
            player.add_card(card, "discard")


###############################################################################
class TestMiller(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g.get_card_from_pile("Townsfolk")
            if self.card.name == "Miller":
                break
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a miller"""
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Silver", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
