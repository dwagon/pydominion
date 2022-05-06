#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Rabble(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = """+3 cards. Each other player reveals the top 3 cards of his
            deck, discards the revealed Actions and Treasures, and puts the rest
            back on top in any order he chooses."""
        self.name = "Rabble"
        self.cost = 5
        self.cards = 3

    def attack(self, victim, attacker):
        cards = []
        for _ in range(3):
            c = victim.next_card()
            victim.reveal_card(c)
            if c.isAction() or c.isTreasure():
                victim.output(
                    "Discarding %s due to %s's rabble" % (c.name, attacker.name)
                )
                attacker.output("%s discarding %s" % (victim.name, c.name))
                victim.discard_card(c)
            else:
                cards.append(c)
        # TODO - let victim pick order
        for c in cards:
            victim.output("Putting %s back on deck" % c.name)
            attacker.output("%s keeping %s" % (victim.name, c.name))
            victim.add_card(c, "deck")

    def special(self, game, player):
        """Each other player reveals the top 3 cards of his deck,
        discard the revealed Actions and Treasures, and puts the
        rest back on top in any order he chooses"""
        for plr in player.attack_victims():
            self.attack(plr, player)


###############################################################################
class Test_Rabble(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Rabble", "Moat"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.rabble = self.g["Rabble"].remove()
        self.moat = self.g["Moat"].remove()
        self.attacker.add_card(self.rabble, "hand")

    def test_defended(self):
        self.victim.add_card(self.moat, "hand")
        self.attacker.play_card(self.rabble)
        self.assertEqual(self.victim.hand.size(), 6)  # 5 + moat
        self.assertEqual(self.attacker.hand.size(), 5 + 3)
        self.assertTrue(self.victim.discardpile.is_empty())

    def test_nodefense(self):
        self.victim.deck.set("Copper", "Estate", "Rabble")
        self.attacker.play_card(self.rabble)
        self.assertEqual(self.victim.deck[-1].name, "Estate")
        self.assertEqual(self.victim.discardpile.size(), 2)
        self.assertEqual(self.attacker.hand.size(), 5 + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
