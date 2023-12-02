#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Poorhouse(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+4 Coin. Reveal your hand. -1 Coin per Treasure card in your hand, to a minimum of 0."""
        self.name = "Poor House"
        self.cost = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        coins = 4
        for card in player.piles[Piles.HAND]:
            player.reveal_card(card)
            if card.isTreasure():
                coins -= 1
        player.output("Gaining %d coins" % max(coins, 0))
        player.coins.add(max(coins, 0))


###############################################################################
class Test_Poorhouse(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Poor House"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Poor House")

    def test_play(self) -> None:
        """Play an Poor House"""
        self.plr.piles[Piles.HAND].set("Estate", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 4 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
