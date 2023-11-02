#!/usr/bin/env python
import contextlib
import unittest
from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Raze(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Action; Trash this or a card from your hand. Look at a number
            of cards from the top of your deck equal to the cost in Coin of the
            trashed card. Put one into your hand and discard the rest """
        self.name = "Raze"
        self.actions = 1
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash this or a card from your hand. Look at a number of cards
        from the top of your deck equal to the cost in Coin of the trashed
        card. Put one into your hand and discard the rest"""
        cards_to_trash: list[Card.Card] = [self]
        for card in player.piles[Piles.HAND]:
            cards_to_trash.append(card)
        trash = player.plr_trash_card(cardsrc=cards_to_trash, force=True)
        cost = trash[0].cost
        if not cost:
            return
        cards = []
        for _ in range(cost):
            with contextlib.suppress(NoCardException):
                cards.append(player.next_card())
        ans = player.card_sel(
            force=True, prompt="Pick a card to put into your hand", cardsrc=cards
        )
        for card in cards:
            if card == ans[0]:
                player.add_card(card, Piles.HAND)
            else:
                player.add_card(card, Piles.DISCARD)


###############################################################################
class Test_Raze(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Raze"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Raze")

    def test_play(self) -> None:
        """Play a card - trashing itself"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province")
        self.plr.test_input = ["Raze", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Raze", self.g.trash_pile)

    def test_copper(self) -> None:
        """Play a card - trashing copper - a zero value card"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province")
        self.plr.test_input = ["Copper", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
