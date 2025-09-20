#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Apprentice(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "+1 action, Trash a card, +1 card per coin it costs, +2 cards if it has a potion cost"
        self.name = "Apprentice"
        self.cost = 5
        self.actions = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash a card from your hand. +1 Card per coin it costs.
        +2 Cards if it has potion it its cost"""
        tc = player.plr_trash_card()
        if not tc:
            return
        c = tc[0]
        numcards = c.cost
        if c.potcost:
            numcards += 2
        player.pickup_cards(numcards)


###############################################################################
class Test_Apprentice(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Apprentice", "Familiar"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.apprentice = self.g.get_card_from_pile("Apprentice")

    def test_trash_none(self) -> None:
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.apprentice, Piles.HAND)
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.apprentice)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_trash_card(self) -> None:
        self.plr.piles[Piles.HAND].set("Silver")
        self.plr.add_card(self.apprentice, Piles.HAND)
        self.plr.test_input = ["silver"]
        self.plr.play_card(self.apprentice)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), self.g.trash_pile[-1].cost)

    def test_trash_potion(self) -> None:
        self.plr.piles[Piles.HAND].set("Familiar")
        self.plr.add_card(self.apprentice, Piles.HAND)
        self.plr.test_input = ["Familiar"]
        self.plr.play_card(self.apprentice)
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), self.g.trash_pile[-1].cost + 2
        )


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
