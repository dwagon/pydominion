#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fellowship_of_Scribes """

import unittest
from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_Fellowship_of_Scribes(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = (
            """After playing an Action, if you have 4 or fewer cards in hand, you may spend a Favor for +1 Card."""
        )
        self.name = "Fellowship of Scribes"

    def hook_post_action(self, game, player, card):
        if not player.favors.get():
            return
        if player.piles[Piles.HAND].size() > 4:
            return
        choice = player.plr_choose_options(
            "Use Fellowship of Scribes to spend a favor to pickup a card?",
            ("Gain a card", "gain"),
            ("No thanks", "no"),
        )
        if choice == "gain":
            player.pickup_card()
            player.favors.add(-1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Fellowship_of_Scribes(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ally="Fellowship of Scribes",
            initcards=["Festival", "Underling"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Play and gain a card"""
        self.card = self.g.get_card_from_pile("Festival")
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.favors.set(2)
        self.plr.test_input = ["Gain"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.favors.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1 + 1)

    def test_play_no_gain(self):
        """Play and don't gain a card"""
        self.card = self.g.get_card_from_pile("Festival")
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.favors.set(2)
        self.plr.test_input = ["No"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.favors.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
