#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Town_Crier"""
import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Town_Crier(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TOWNSFOLK]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 2
        self.name = "Town Crier"
        self.desc = """Choose one: +$2; or gain a Silver;
                or +1 Card and +1 Action.
                You may rotate the Townsfolk."""
        self.pile = "Townsfolk"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        opt = player.plr_choose_options(
            "Choose One: ",
            ("+$2", "cash"),
            ("Gain a Silver", "silver"),
            ("+1 Card and +1 action", "card"),
        )
        if opt == "cash":
            player.coins.add(2)
        elif opt == "silver":
            try:
                player.gain_card("Silver")
            except NoCardException:  # pragma: no coverage
                player.output("No more Silvers")
        elif opt == "card":
            player.pickup_cards(1)
            player.add_actions(1)
        opt = player.plr_choose_options(
            "Do you want to rotate the Townsfolk?",
            ("Don't change", False),
            ("Rotate", True),
        )
        if opt:
            game.card_piles["Townsfolk"].rotate()


###############################################################################
class TestTownCrier(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g.get_card_from_pile("Townsfolk")
            if self.card.name == "Town Crier":
                break
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_rotate_cash(self) -> None:
        """Play a town crier - rotate, but get cash"""
        self.plr.test_input = ["+$2", "Rotate"]
        cns = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), cns + 2)
        card = self.g.get_card_from_pile("Townsfolk")
        self.assertEqual(card.name, "Blacksmith")

    def test_play_retain_silver(self) -> None:
        """Play a town crier - don't rotate, but get silver"""
        self.plr.test_input = ["Silver", "Don't"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        card = self.g.get_card_from_pile("Townsfolk")
        self.assertEqual(card.name, "Town Crier")

    def test_play_retain_card(self) -> None:
        """Play a town crier - don't rotate, but get card and action"""
        self.plr.test_input = ["card", "Don't"]
        hndsze = self.plr.piles[Piles.HAND].size()
        acts = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsze + 1 - 1)
        self.assertEqual(self.plr.actions.get(), acts + 1 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
