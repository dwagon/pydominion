#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Forest_Dwellers"""

import unittest
from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_ForestDwellers(Ally.Ally):
    """Forest Dwellers"""

    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your turn, you may spend a Favor to look at the top 3 cards of your deck, 
        discard any number and put the rest back in any order."""
        self.name = "Forest Dwellers"

    def hook_start_turn(self, game, player):
        """ """
        if player.favors.get() < 1:
            return
        do_it = player.plr_choose_options(
            "Forest Dwellers:",
            ("Do nothing", False),
            (
                "Spend a favour to look at the top 3 cards of your deck, discard any number?",
                True,
            ),
        )
        if do_it:
            player.favors.add(-1)
            cards = [player.next_card() for _ in range(3)]
            player.output(f"Cards are: {', '.join([_.name for _ in cards])}")
            for card in cards:
                options = [(f"Discard {card}", True), (f"Keep {card} on deck", False)]
                opt = player.plr_choose_options(f"For {card} choose to", *options)
                if opt:
                    player.add_card(card, Piles.DISCARD)
                else:
                    player.add_card(card, Piles.DECK)


###############################################################################
def botresponse(
    player, kind, args=None, kwargs=None
):  # pylint: disable=unused-argument
    """Bot response - just do nothing"""
    return False


###############################################################################
class Test_ForestDwellers(unittest.TestCase):
    """Test Forest Dwellers"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, allies="Forest Dwellers", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self):
        """Play and gain a card"""
        self.plr.piles[Piles.DECK].set("Gold", "Silver", "Copper")
        self.plr.favors.set(2)
        self.plr.test_input = [
            "Spend a favour",
            "Discard Copper",
            "Discard Silver",
            "Keep Gold",
        ]
        self.plr.start_turn()
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.favors.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
