#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, Phase, NoCardException


###############################################################################
class Card_Doctor(Card.Card):
    """Doctor"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.name = "Doctor"
        self.overpay = True
        self.cost = 3

    def dynamic_description(self, player: Player.Player) -> str:
        """Variable description"""
        if player.phase == Phase.BUY:
            return """Name a card. Reveal the top 3 cards of your deck.
                Trash the matches. Put the rest back on top in any order.
                When you buy this, you may overpay for it. For each 1 you overpaid,
                look at the top card of your deck; trash it, discard it,
                or put it back."""
        return """Name a card. Reveal the top 3 cards of your deck.
            Trash the matches. Put the rest back on top in any order."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        choices = []
        for name, pile in sorted(game.get_card_piles()):
            choices.append((f"Guess {name}", name))
        o = player.plr_choose_options("Pick which card to trash if it is in the top 3 of your deck", *choices)

        cards: list[Card.Card] = []
        for _ in range(3):
            try:
                cards.append(player.next_card())
            except NoCardException:  # pragma: no coverage
                break

        for card in cards:
            player.reveal_card(card)
            if card.name == o:
                player.output(f"Trashing {card}")
                card.location = None
                player.trash_card(card)
            else:
                player.output(f"Putting {card} back")
                player.add_card(card, Piles.DECK)

    def hook_overpay(self, game: "Game.Game", player: "Player.Player", amount: int) -> None:
        """For each 1 you overpaid, look at the top card of your deck; trash it,
        discard it, or put it back."""
        for i in range(amount):
            player.output(f"Doctoring {i+1}/{amount}")
            try:
                card = player.next_card()
            except NoCardException:  # pragma: no coverage
                continue
            choices = [
                (f"Put {card} back on top", "put back"),
                (f"Trash {card}", "trash"),
                (f"Discard {card}", "discard"),
            ]
            choice = player.plr_choose_options(f"What to do with the top card {card}?", *choices)
            if choice == "trash":
                card.location = None
                player.trash_card(card)
                player.output(f"Trashing {card}")
            elif choice == "discard":
                player.add_card(card, Piles.DISCARD)
                player.output(f"Discarding {card}")
            elif choice == "put back":
                player.add_card(card, Piles.DECK)
                player.output(f"Putting {card} back")


###############################################################################
class TestDoctor(unittest.TestCase):
    """Test Doctor"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Doctor"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Doctor")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play the Doctor"""
        self.plr.piles[Piles.DECK].set("Silver", "Province", "Duchy")
        self.plr.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertIn("Province", self.g.trash_pile)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Duchy", self.plr.piles[Piles.DECK])

    def test_buy(self) -> None:
        """Buy a Doctor"""
        self.plr.coins.set(6)
        self.plr.test_input = ["3", "trash", "discard", "back on top"]
        self.plr.piles[Piles.DECK].set("Silver", "Province", "Duchy")
        self.plr.buy_card("Doctor")
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
