#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Sorcerer(Card.Card):
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

    def _generate_options(self, game):
        """Generate the options for user interaction"""
        options = []
        for name, card_pile in game.card_piles():
            card = game.get_card_from_pile(name)
            if card and card.purchasable:
                options.append((name, name))
        return options

    def special(self, game, player):
        for plr in player.attack_victims():
            options = self._generate_options(game)
            pick = plr.plr_choose_options(
                "Sorcerer: Guess the top card correctly or get a curse", *options
            )
            top_card = plr.piles[Piles.DECK].top_card()
            player.reveal_card(top_card)
            if top_card.name != pick:
                player.output(f"Top card is {top_card.name} not {pick}")
                plr.gain_card("Curse")
            else:
                player.output(f"Guessed {pick} correctly")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    """Possibly not the best guess, but might be good enough"""
    return "Copper"


###############################################################################
class TestSorcerer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Wizards"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play_hit(self):
        card = self.g.get_card_from_pile("Wizards", "Sorcerer")
        self.plr.add_card(card, Piles.HAND)
        hndsz = self.plr.piles[Piles.HAND].size()
        self.vic.piles[Piles.DECK].set("Duchy")
        self.vic.test_input = ["Duchy"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsz)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertNotIn("Curse", self.vic.piles[Piles.DISCARD])

    def test_play_miss(self):
        while True:
            card = self.g["Wizards"].remove()
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
