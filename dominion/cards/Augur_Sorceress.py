#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Sorceress"""


import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Sorceress(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.AUGUR]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 5
        self.actions = 1
        self.required_cards = ["Curse"]
        self.name = "Sorceress"
        self.desc = """+1 Action; Name a card. Reveal the top card of your deck
            and put it into your hand. If it's the named card, each other player
            gains a Curse."""
        self.pile = "Augurs"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            card = player.pickup_card()
        except NoCardException:
            return
        choices: list[tuple[str, Any]] = [("No guess", None)]
        for name, _ in sorted(game.get_card_piles()):
            choices.append((f"Guess {name}", name))
        guess = player.plr_choose_options("Guess the top card", *choices)
        if not guess:
            player.output("No suitable cards")
            return

        player.output(f"Next card = {card}, Guess = {guess}")
        if card.name == guess:
            game.output(f"Guessed {card} correctly")
            for plr in player.attack_victims():
                try:
                    plr.gain_card("Curse")
                except NoCardException:
                    player.output("No more Curses")
                    break


###############################################################################
class TestSorceress(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Augurs"], badcards=["Gold Mine"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g.get_card_from_pile("Augurs")
            if card.name == "Sorceress":
                break
        self.card = card
        self.plr.add_card(self.card, Piles.HAND)

    def test_good_guess(self) -> None:
        """Play a sorceress and guess correctly"""
        self.plr.piles[Piles.DECK].set("Gold", "Gold")
        self.plr.test_input = ["Guess Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
