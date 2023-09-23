#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Journeyman"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Journeyman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = """Name a card.
        Reveal cards from the top of your deck until you reveal 3 cards that are not the named card.
        Put those cards into your hand and discard the rest."""
        self.name = "Journeyman"
        self.cost = 5

    def special(self, game, player):
        options = [{"selector": "0", "print": "No guess", "card": None}]
        index = 1
        for name, card_pile in sorted(game.get_card_piles()):
            options.append(
                {"selector": f"{index}", "print": f"Guess {name}", "card": name}
            )
            index += 1
        o = player.user_input(
            options,
            "Name a card. Reveal cards from your deck until you have 3 that aren't the named card",
        )
        if o["card"] is None:
            return
        cards = []
        while len(cards) < 3:
            card = player.next_card()
            player.reveal_card(card)
            if card.name == o["card"]:
                player.output(f"Discarding {card}")
                player.discard_card(card)
            else:
                cards.append(card)
        for card in cards:
            player.add_card(card, Piles.HAND)
            player.output(f"Pulling {card} into hand")


###############################################################################
class TestJourneyman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Journeyman"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Journeyman")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        """Play the pawn - select card and action"""
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Duchy", "Province", "Gold")
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])

    def test_play_guess_none(self):
        """Chose not to guess"""
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Duchy", "Province", "Gold")
        self.plr.test_input = ["No guess"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Province", self.plr.piles[Piles.DECK])
        self.assertIn("Estate", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
