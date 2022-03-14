#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Gladiator(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.EMPIRES
        self.desc = """+2 Coin
        Reveal a card from your hand. The player to your left may reveal a copy from their hand.
        If they do not, +1 Coin and trash a Gladiator from the Supply."""
        self.name = "Gladiator"
        self.cost = 3
        self.coin = 2
        self.numcards = 5
        self.split = "Fortune"

    def special(self, game, player):
        mycard = player.cardSel(
            num=1,
            force=True,
            prompt="Select a card from your hand that the player to your left doesn't have",
        )
        player.reveal_card(mycard[0])
        lefty = game.playerToLeft(player)
        leftycard = lefty.in_hand(mycard[0].name)
        if not leftycard:
            player.output("%s doesn't have a %s" % (lefty.name, mycard[0].name))
            player.addCoin(1)
            c = game["Gladiator"].remove()
            player.trash_card(c)
        else:
            player.output("%s has a %s" % (lefty.name, mycard[0].name))
            lefty.reveal_card(leftycard)


###############################################################################
class Test_Gladiator(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Gladiator", "Moat"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Gladiator"].remove()

    def test_play_nothave(self):
        """Play a Gladiator - something the other player doesn't have"""
        self.plr.set_hand("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Gladiator"))
        self.assertEqual(self.plr.getCoin(), 3)

    def test_play_has(self):
        """Play a Gladiator - something the other player has"""
        self.plr.set_hand("Moat", "Copper", "Estate")
        self.vic.set_hand("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.assertIsNone(self.g.in_trash("Gladiator"))
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
