#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Horse """

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Horse(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards; +1 Action; Return this to its pile."
        self.name = "Horse"
        self.purchasable = False
        self.insupply = False
        self.actions = 1
        self.cards = 2
        self.cost = 0
        self.numcards = 30

    def special(self, game: Game.Game, player: Player.Player) -> None:
        # Things like Throne Room can change the location
        if self.location not in (None, Piles.CARDPILE):
            player.move_card(self, Piles.CARDPILE)


###############################################################################
class TestHorse(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Horse"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Horse")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertNotIn("Horse", self.plr.piles[Piles.PLAYED])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
