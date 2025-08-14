#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Good_Harvest"""

import unittest
from collections import Counter

from dominion import Card, Game, Prophecy, Player, OptionKeys, Piles


###############################################################################
class Prophecy_Good_Harvest(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "The first time you play each differently named Treasure each turn, first, +1 Buy and +$1."
        self.name = "Good Harvest"

    def hook_post_play(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, str]:
        if card.isTreasure():
            counts = Counter[str]()
            for _ in player.piles[Piles.PLAYED]:
                counts[_.name] += 1
            if counts[card.name] == 1:  # Just played card
                player.buys.add(1)
                player.coins.add(1)
                player.output("Good Harvest adds buy and $")
        return {}


###############################################################################
class Test_Good_Harvest(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Good Harvest"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active"""
        self.plr.piles[Piles.HAND].set()
        au_1 = self.g.get_card_from_pile("Gold")
        self.plr.add_card(au_1, Piles.HAND)
        au_2 = self.g.get_card_from_pile("Gold")
        self.plr.add_card(au_2, Piles.HAND)
        ag_1 = self.g.get_card_from_pile("Silver")
        self.plr.add_card(ag_1, Piles.HAND)

        # Play Gold first time
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        self.plr.play_card(au_1)
        self.assertEqual(self.plr.coins.get(), coins + 3 + 1)
        self.assertEqual(self.plr.buys.get(), buys + 1)

        # Play Gold second time - no benefit expected
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        self.plr.play_card(au_2)
        self.assertEqual(self.plr.coins.get(), coins + 3)
        self.assertEqual(self.plr.buys.get(), buys)

        # Play Silver first time
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        self.plr.play_card(ag_1)
        self.assertEqual(self.plr.coins.get(), coins + 2 + 1)
        self.assertEqual(self.plr.buys.get(), buys + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
