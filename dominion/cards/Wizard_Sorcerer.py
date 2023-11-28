#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Sorcerer"""
import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Sorcerer(Card.Card):
    """Sorcerer"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.WIZARD,  # pylint: disable=no-member
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 5
        self.cards = 1
        self.required_cards = ["Curse"]
        self.actions = 1
        self.name = "Sorcerer"
        self.pile = "Wizards"
        self.desc = """+1 Card; +1 Action; Each other player names a card,
            then reveals the top card of their deck. If wrong, they gain a Curse."""

    def _generate_options(self, game: Game.Game) -> list[tuple[str, str]]:
        """Generate the options for user interaction"""
        options: list[tuple[str, str]] = []
        for name, card_pile in game.get_card_piles():
            card = game.card_instances[name]
            if card and card.purchasable:
                options.append((name, name))
        return options

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for plr in player.attack_victims():
            options = self._generate_options(game)
            pick = plr.plr_choose_options(
                "Sorcerer: Guess the top card correctly or get a curse", *options
            )
            try:
                top_card = plr.piles[Piles.DECK].top_card()
            except NoCardException:
                player.output("No cards in deck")
                continue
            player.reveal_card(top_card)
            if top_card.name != pick:
                player.output(f"Top card is {top_card} not {pick}")
                try:
                    plr.gain_card("Curse")
                except NoCardException:
                    player.output("No more Curses")
            else:
                player.output(f"Guessed {pick} correctly")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    """Possibly not the best guess, but might be good enough"""
    return "Copper"


###############################################################################
class TestSorcerer(unittest.TestCase):
    """Test Sorcerer"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Wizards"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play_hit(self) -> None:
        card = self.g.get_card_from_pile("Wizards", "Sorcerer")
        self.plr.add_card(card, Piles.HAND)
        hndsz = self.plr.piles[Piles.HAND].size()
        self.vic.piles[Piles.DECK].set("Duchy")
        self.vic.test_input = ["Duchy"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsz)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertNotIn("Curse", self.vic.piles[Piles.DISCARD])

    def test_play_miss(self) -> None:
        while True:
            card = self.g.get_card_from_pile("Wizards")
            if card.name == "Sorcerer":
                break
        self.plr.add_card(card, Piles.HAND)
        hndsz = self.plr.piles[Piles.HAND].size()
        self.vic.piles[Piles.DECK].set("Duchy")
        self.vic.test_input = ["Estate"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsz)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
