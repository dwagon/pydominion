#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Gladiator(Card.Card):
    """Gladiator"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+2 Coin
        Reveal a card from your hand. The player to your left may reveal a copy from their hand.
        If they do not, +1 Coin and trash a Gladiator from the Supply."""
        self.name = "Gladiator"
        self.cost = 3
        self.coin = 2
        self.numcards = 5
        self.split = "Fortune"

    def special(self, game, player):
        if not player.piles[Piles.HAND]:
            return
        mycard = player.card_sel(
            num=1,
            force=True,
            prompt="Select a card from your hand that the player to your left doesn't have",
        )
        player.reveal_card(mycard[0])
        lefty = game.player_to_left(player)
        leftycard = lefty.piles[Piles.HAND][mycard[0].name]
        if not leftycard:
            player.output(f"{lefty.name} doesn't have a {mycard[0].name}")
            player.coins.add(1)
            c = game.card_piles["Gladiator"].remove()
            if c:
                player.trash_card(c)
        else:
            player.output(f"{lefty.name} has a {mycard[0].name}")
            lefty.reveal_card(leftycard)


###############################################################################
class TestGladiator(unittest.TestCase):
    """Test Gladiator"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Gladiator", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Gladiator")

    def test_play_nothave(self):
        """Play a Gladiator - something the other player doesn't have"""
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Gladiator", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 3)

    def test_play_has(self):
        """Play a Gladiator - something the other player has"""
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.vic.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertNotIn("Gladiator", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
