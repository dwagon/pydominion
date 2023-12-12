#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Band_of_misfits"""

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_BandOfMisfits(Card.Card):
    """Band of Misfits"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.COMMAND]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Play a non-Command Action card from the Supply that costs
            less than this, leaving it there."""
        self.name = "Band of Misfits"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        options = []
        for action_pile in game.get_action_piles(self.cost - 1):
            options.append((f"Select {action_pile}", action_pile))
        if not options:  # pragma: no coverage
            player.output("No suitable cards")
            return
        choice = player.plr_choose_options(
            "What action card do you want to play?", *options
        )
        action = game.card_instances[choice]
        player.card_benefits(action)
        # If the card moved itself somewhere
        if action.location and action.location != Piles.CARDPILE:
            player.remove_card(action)


###############################################################################
class TestBandOfMisfits(unittest.TestCase):
    """Test Band of Misfits"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            initcards=[
                "Band of Misfits",
                "Village",
                "Bureaucrat",
                "Moat",
                "Acting Troupe",
            ],
            badcards=["Village Green"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Band of Misfits")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_bureaucrat(self) -> None:
        """Make the Band of Misfits be a Bureaucrat"""
        self.plr.test_input = ["Bureaucrat"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])

    def test_play_village(self) -> None:
        """Make the Band of Misfits be a Village"""
        self.plr.test_input = ["Select Village"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_play_acting_troupe(self) -> None:
        """Play with a card that trashes itself"""
        stack_size = len(self.g.card_piles["Acting Troupe"])
        self.plr.test_input = ["Select Acting Troupe"]
        self.plr.play_card(self.card)
        self.assertNotIn("Acting Troupe", Piles.TRASH)
        self.assertEqual(len(self.g.card_piles["Acting Troupe"]), stack_size)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
