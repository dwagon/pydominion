#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fellowship_of_Scribes """

import unittest

from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_Fellowship_of_Scribes(Ally.Ally):
    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """After playing an Action, if you have 4 or fewer cards in hand, you may spend a Favor for +1 Card."""
        self.name = "Fellowship of Scribes"

    def hook_post_play(self, game, player, card):
        if not player.favors.get():
            return
        if player.piles[Piles.HAND].size() > 4:
            return
        if player.plr_choose_options(
            "Use Fellowship of Scribes to spend a favor to pickup a card?",
            ("Gain a card", True),
            ("No thanks", False),
        ):
            player.pickup_cards(1)
            player.favors.add(-1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Fellowship_of_Scribes(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            allies="Fellowship of Scribes",
            initcards=["Festival", "Underling"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
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

    def test_play_no_gain(self) -> None:
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
