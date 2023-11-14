#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Coven """

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Coven(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+1 Action; +2 Coin; Each other player Exiles a Curse
            from the Supply. If they can't, they discard their Exiled Curses."""
        self.name = "Coven"
        self.actions = 1
        self.coin = 2
        self.cost = 5
        self.required_cards = ["Curse"]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for plr in player.attack_victims():
            plr.exile_card_from_supply("Curse")
            if game.card_piles["Curse"].is_empty():
                num = plr.unexile("Curse")
                plr.output(f"Unexiled {num} Curses from {player}'s Coven")
            else:
                plr.output(f"Exiled a Curse from {player}'s Coven")


###############################################################################
class TestCoven(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Coven", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Coven")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Curse", self.vic.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
