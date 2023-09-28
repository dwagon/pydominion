#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Rocks"""
import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Rocks(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Rocks"
        self.coin = 1
        self.cost = 4
        self.pile = "Catapult"
        self.desc = """$1; When you gain or trash this: If it's your Buy phase, gain a Silver onto your deck,
        otherwise gain a Silver to your hand."""

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        self.rocks_special(player)

    ###########################################################################
    def hook_trashThisCard(self, game, player):
        self.rocks_special(player)

    ###########################################################################
    def rocks_special(self, player):
        if player.phase == Player.Phase.BUY:
            player.gain_card("Silver", Piles.DECK)
        else:
            player.gain_card("Silver", Piles.HAND)


###############################################################################
class Test_Rocks(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Catapult"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_gain_rocks(self):
        """Gain a Rocks"""
        for _ in range(5):
            self.plr.gain_card("Catapult")  # Get these out of the way
        self.plr.phase = Player.Phase.BUY
        self.plr.gain_card("Rocks")
        self.assertIn("Silver", self.plr.piles[Piles.DECK])

    def test_play_rocks(self):
        """Play a rocks"""
        coins = self.plr.coins.get()
        card = self.g.get_card_from_pile("Catapult", "Rocks")
        self.plr.add_card(card, Piles.HAND)
        self.plr.play_card(card)
        self.assertEqual(self.plr.coins.get(), coins + 1)

    def test_trash_rocks(self):
        """Trash a rocks"""
        card = self.g.get_card_from_pile("Catapult", "Rocks")
        self.plr.trash_card(card)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF