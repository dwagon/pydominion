#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Spy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DOMINION
        self.desc = "+1 action, +1 cards, reveal next card and optionally discard it"
        self.name = "Spy"
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """Each player (including you) reveals the top of his deck and either discards it or puts it back, your choice"""
        self.spyOn(player, player)
        for pl in player.attackVictims():
            self.spyOn(player, pl)

    def spyOn(self, attacker, victim):
        c = victim.next_card()
        victim.reveal_card(c)
        vicname = "your" if attacker == victim else "%s's" % victim.name
        discard = attacker.plrChooseOptions(
            "Discard %s card?" % vicname,
            ("Keep %s on %s deck" % (c.name, vicname), False),
            ("Discard %s %s" % (vicname, c.name), True),
        )
        if discard:
            victim.addCard(c, "discard")
            victim.output("%s's Spy discarded your %s" % (attacker.name, c.name))
        else:
            victim.addCard(c, "topdeck")


###############################################################################
class Test_Spy(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Spy", "Moat"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.attacker.set_deck("Estate", "Province", "Duchy")
        self.defender.set_deck("Estate", "Gold")

    def test_moat(self):
        self.defender.set_hand("Moat")
        scard = self.attacker.gainCard("Spy", "hand")
        self.attacker.test_input = ["0"]
        self.attacker.playCard(scard)
        self.assertEqual(self.attacker.deck[-1].name, "Province")
        self.assertEqual(self.defender.deck[-1].name, "Gold")

    def test_undefended(self):
        scard = self.attacker.gainCard("Spy", "hand")
        self.attacker.test_input = ["0", "0"]
        self.attacker.playCard(scard)
        self.assertEqual(self.attacker.deck[-1].name, "Province")
        self.assertEqual(self.defender.deck[-1].name, "Gold")

    def test_discards(self):
        scard = self.attacker.gainCard("Spy", "hand")
        self.attacker.test_input = ["1", "1"]
        self.attacker.playCard(scard)
        self.assertEqual(self.attacker.deck[-1].name, "Estate")
        self.assertEqual(self.defender.deck[-1].name, "Estate")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
