#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_NightWatchman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT]
        self.base = Game.NOCTURNE
        self.desc = "Look at the top 5 cards of your deck, discard any number, and put the rest back in any order."
        self.name = "Night Watchman"
        self.cost = 3

    def night(self, game, player):
        cards = []
        for _ in range(5):
            c = player.next_card()
            cards.append(c)
        player.output(
            "Top 5 cards on the deck are: %s" % ", ".join([_.name for _ in cards])
        )
        for c in cards:
            discard = player.plr_choose_options(
                "What do you want to do?",
                (f"Discard {c.name}", True),
                (f"Return {c.name} to the deck", False),
            )
            if discard:
                player.discard_card(c)
            else:
                player.add_card(c, "topdeck")

    def hook_gain_this_card(self, game, player):
        return {"destination": "hand"}


###############################################################################
class Test_NightWatchman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Night Watchman"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Night Watchman"].remove()

    def test_play(self):
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.set_deck("Gold", "Province", "Gold", "Duchy", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = [
            "Return Silver",
            "Discard Duchy",
            "Return Gold",
            "Discard Province",
            "Return Gold",
        ]
        self.plr.play_card(self.card)
        try:
            self.assertIn("Duchy", self.plr.discardpile)
            self.assertIn("Province", self.plr.discardpile)
            self.assertNotIn("Gold", self.plr.discardpile)
            self.assertNotIn("Silver", self.plr.discardpile)

            self.assertNotIn("Duchy", self.plr.deck)
            self.assertNotIn("Province", self.plr.deck)
            self.assertIn("Gold", self.plr.deck)
            self.assertIn("Silver", self.plr.deck)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
