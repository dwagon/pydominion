#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Figurine"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Figurine(Card.Card):
    """Figurine"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "+2 Cards; You may discard an Action card for +1 Buy and +$1."
        self.cards = 2
        self.name = "Figurine"
        self.cost = 5

    def special(self, game, player):
        options = [
            (f"Discard {_}", _) for _ in player.piles[Piles.HAND] if _.isAction()
        ]
        if not options:
            player.output("No suitable cards")
            return
        options.insert(0, ("Do nothing", None))
        answer = player.plr_choose_options("Discard for +1 Buy and $1", *options)
        if answer:
            player.discard_card(answer)
            player.buys.add(1)
            player.coins.add(1)


###############################################################################
class Test_Figurine(unittest.TestCase):
    """Test Figurine"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Figurine", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Figurine")

    def test_play(self):
        """Play a card"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard Moat"]
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(self.plr.coins.get(), coins + 1)

    def test_no_suitable(self):
        """Play with no suitable cards"""
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.add_card(self.card, Piles.HAND)
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), buys)
        self.assertEqual(self.plr.coins.get(), coins)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
