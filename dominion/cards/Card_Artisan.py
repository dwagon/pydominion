#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Artisan(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "Gain a card to your hand costing up to 5 Coin. Put a card from your hand onto your deck."
        self.name = "Artisan"
        self.cost = 6

    def special(self, game, player):
        player.plr_gain_card(5, destination="hand")
        card = player.card_sel(
            force=True,
            cardsrc="hand",
            prompt="Put a card from your hand on top of your deck",
        )
        player.add_card(card[0], "topdeck")
        player.hand.remove(card[0])


###############################################################################
class Test_Artisan(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Artisan", "Festival"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Artisan"].remove()

    def test_play(self):
        self.plr.set_hand("Copper", "Estate", "Silver", "Gold", "Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Get Festival", "Select Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.discardpile.size(), 0)
        self.assertEqual(self.plr.deck[-1].name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
