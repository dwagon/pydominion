#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
from dominion.Player import Phase


###############################################################################
class Card_NightWatchman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Look at the top 5 cards of your deck, discard any number, and put the rest back in any order."
        self.name = "Night Watchman"
        self.cost = 3

    def night(self, game, player):
        cards = []
        for _ in range(5):
            if c := player.next_card():
                cards.append(c)
        player.output(
            f'Top 5 cards on the deck are: {", ".join([_.name for _ in cards])}'
        )
        for c in cards:
            if discard := player.plr_choose_options(
                "What do you want to do?",
                (f"Discard {c.name}", True),
                (f"Return {c.name} to the deck", False),
            ):
                player.discard_card(c)
            else:
                player.add_card(c, "topdeck")

    def hook_gain_this_card(self, game, player):
        return {"destination": Piles.HAND}


###############################################################################
class Test_NightWatchman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Night Watchman"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Night Watchman")

    def test_play(self):
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.DECK].set("Gold", "Province", "Gold", "Duchy", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = [
            "Return Silver",
            "Discard Duchy",
            "Return Gold",
            "Discard Province",
            "Return Gold",
        ]
        self.plr.play_card(self.card)
        try:
            self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
            self.assertIn("Province", self.plr.piles[Piles.DISCARD])
            self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
            self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])

            self.assertNotIn("Duchy", self.plr.piles[Piles.DECK])
            self.assertNotIn("Province", self.plr.piles[Piles.DECK])
            self.assertIn("Gold", self.plr.piles[Piles.DECK])
            self.assertIn("Silver", self.plr.piles[Piles.DECK])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
