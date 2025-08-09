#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Gold_Mine"""
import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Gold_Mine(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Card; +1 Action; +1 Buy; You may gain a Gold and get +4 debt."""
        self.name = "Gold Mine"
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.buys = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may gain a Gold and get +4 debt."""
        if player.plr_choose_options("Gain a Gold for 4 debt?", ("Do nothing", False), ("Gain Gold", True)):
            try:
                player.gain_card("Gold")
            except NoCardException:  # pragma: no coverage
                player.output("No more Gold")
                return
            player.debt.add(4)


###############################################################################
class Test_Gold_Mine(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Gold Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Gold Mine")

    def test_play_gain_gold(self) -> None:
        """Play card"""
        self.plr.add_card(self.card, Piles.HAND)
        debt = self.plr.debt.get()
        self.plr.test_input = ["Gain Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.debt.get(), debt + 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
