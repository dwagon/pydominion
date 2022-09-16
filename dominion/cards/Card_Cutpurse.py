#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Cutpurse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.desc = (
            "+2 coin; Each other player discards a Copper card (or reveals a hand with no Copper)."
        )
        self.name = "Cutpurse"
        self.coin = 2
        self.cost = 4
        self.base = Card.CardExpansion.SEASIDE

    def special(self, game, player):
        """Each other player discard a Copper card (or reveals a
        hand with no copper)."""
        for victim in player.attack_victims():
            c = victim.hand["Copper"]
            if c:
                player.output("%s discarded a copper" % victim.name)
                victim.output("Discarded a copper due to %s's Cutpurse" % player.name)
                victim.discard_card(c)
            else:
                for card in victim.hand:
                    victim.reveal_card(card)
                player.output("%s had no coppers" % victim.name)


###############################################################################
class Test_Cutpurse(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Cutpurse"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Cutpurse"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_coppers(self):
        self.victim.hand.set("Copper", "Copper", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.victim.discardpile[-1].name, "Copper")
        self.assertEqual(self.victim.hand.size(), 2)

    def test_play_none(self):
        self.victim.hand.set("Duchy", "Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertTrue(self.victim.discardpile.is_empty())
        self.assertEqual(self.victim.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
