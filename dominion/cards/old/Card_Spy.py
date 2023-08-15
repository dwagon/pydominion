#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Spy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+1 action, +1 cards, reveal next card and optionally discard it"
        self.name = "Spy"
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """Each player (including you) reveals the top of his deck and either
        discards it or puts it back, your choice"""
        self.spy_on(player, player)
        for pl in player.attack_victims():
            self.spy_on(player, pl)

    def spy_on(self, attacker, victim):
        c = victim.next_card()
        victim.reveal_card(c)
        vicname = "your" if attacker == victim else f"{victim.name}'s"
        discard = attacker.plr_choose_options(
            f"Discard {vicname} card?",
            (f"Keep {c.name} on {vicname} deck", False),
            (f"Discard {vicname} {c.name}", True),
        )
        if discard:
            victim.add_card(c, "discard")
            victim.output("f{attacker.name}'s Spy discarded your {c.name}")
        else:
            victim.add_card(c, "topdeck")


###############################################################################
class TestSpy(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Spy", "Moat"])
        self.g.start_game()
        self.attacker, self.defender = self.g.player_list()
        self.attacker.piles[Piles.DECK].set("Estate", "Province", "Duchy")
        self.defender.piles[Piles.DECK].set("Estate", "Gold")

    def test_moat(self):
        self.defender.piles[Piles.HAND].set("Moat")
        scard = self.attacker.gain_card("Spy", "hand")
        self.attacker.test_input = ["0"]
        self.attacker.play_card(scard)
        self.assertEqual(self.attacker.piles[Piles.DECK][-1].name, "Province")
        self.assertEqual(self.defender.piles[Piles.DECK][-1].name, "Gold")

    def test_undefended(self):
        scard = self.attacker.gain_card("Spy", "hand")
        self.attacker.test_input = ["0", "0"]
        self.attacker.play_card(scard)
        self.assertEqual(self.attacker.piles[Piles.DECK][-1].name, "Province")
        self.assertEqual(self.defender.piles[Piles.DECK][-1].name, "Gold")

    def test_discards(self):
        scard = self.attacker.gain_card("Spy", "hand")
        self.attacker.test_input = ["1", "1"]
        self.attacker.play_card(scard)
        self.assertEqual(self.attacker.piles[Piles.DECK][-1].name, "Estate")
        self.assertEqual(self.defender.piles[Piles.DECK][-1].name, "Estate")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
