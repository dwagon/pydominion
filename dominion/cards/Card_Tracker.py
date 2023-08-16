#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Tracker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Coin, Receive a boon; While this is in play, when you gain a card, you may put that card onto your deck"
        self.name = "Tracker"
        self.cost = 2
        self.coin = 1
        self.heirloom = "Pouch"

    def special(self, game, player):
        # Special flag to stop boon interfering with tests
        if not hasattr(player, "_tracker_dont_boon"):
            player.receive_boon()

    def hook_gain_card(self, game, player, card):
        """While this is in play, when you gain a card, you may
        put that card on top of your deck"""
        mod = {}
        deck = player.plr_choose_options(
            "Where to put %s?" % card.name,
            ("Put %s on discard" % card.name, False),
            ("Put %s on top of deck" % card.name, True),
        )
        if deck:
            player.output("Putting %s on deck due to Tracker" % card.name)
            mod["destination"] = "topdeck"
        return mod


###############################################################################
class Test_Tracker(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Tracker"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.plr._tracker_dont_boon = True
        self.card = self.g["Tracker"].remove()

    def test_play(self):
        """Play a Tracker"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.coins.get(), 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_discard(self):
        """Have a Tracker  - discard the gained card"""
        self.plr.piles[Piles.PLAYED].set("Tracker")
        self.plr.test_input = ["discard"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])

    def test_deck(self):
        """Have a Tracker  - the gained card on the deck"""
        self.plr.piles[Piles.PLAYED].set("Tracker")
        self.plr.test_input = ["deck"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
