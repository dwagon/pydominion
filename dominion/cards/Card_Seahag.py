#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


class Card_Seahag(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.SEASIDE
        self.desc = "Each other player discards the top card of his deck, then gains a Curse card, putting it on top of his deck"
        self.required_cards = ["Curse"]
        self.name = "Sea Hag"
        self.cost = 4

    def special(self, game, player):
        """Each other player discards the top card of his deck,
        then gains a Curse card, putting it on top of his deck"""
        for pl in player.attackVictims():
            c = pl.nextCard()
            pl.discardCard(c)
            pl.output("Discarded your %s" % c.name)
            pl.gainCard("Curse", destination="topdeck")
            pl.output("Got cursed by %s's Sea Hag" % player.name)
            player.output("%s got cursed" % pl.name)


###############################################################################
class Test_Seahag(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Sea Hag", "Moat"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.seahag = self.g["Sea Hag"].remove()
        self.mcard = self.g["Moat"].remove()
        self.attacker.addCard(self.seahag, "hand")

    def test_defended(self):
        self.victim.addCard(self.mcard, "hand")
        self.attacker.playCard(self.seahag)
        self.assertEqual(self.victim.hand.size(), 6)
        self.assertNotEqual(self.victim.deck[0].name, "Curse")
        self.assertTrue(self.victim.discardpile.is_empty())

    def test_nodefense(self):
        self.victim.setDeck("Gold")
        self.attacker.playCard(self.seahag)
        self.assertEqual(self.victim.hand.size(), 5)
        self.assertEqual(self.victim.discardpile[0].name, "Gold")
        self.assertEqual(self.victim.deck[0].name, "Curse")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
