#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_CouncilRoom(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+4 cards, +1 buy. Everyone else +1 card"
        self.name = "Council Room"
        self.cards = 4
        self.buys = 1
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each other player draws a card"""
        for pl in game.player_list():
            if pl != player:
                pl.output(
                    f"Picking up card due to {player.name} playing a Council Room"
                )
                try:
                    pl.pickup_card()
                except NoCardException:
                    pass


###############################################################################
class TestCouncilRoom(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Council Room"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.ccard = self.g.get_card_from_pile("Council Room")
        self.plr.add_card(self.ccard, Piles.HAND)

    def test_play(self) -> None:
        self.assertEqual(self.other.piles[Piles.HAND].size(), 5)
        self.plr.play_card(self.ccard)
        self.assertEqual(self.other.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 9)
        self.assertEqual(self.plr.buys.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
