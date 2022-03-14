#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


class Card_Bureaucrat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.DOMINION
        self.desc = """ Gain a Silver; put it on top of your deck. Each
            other player reveals a victory card from his hand and puts
            it on his deck (or reveals a hand with no victory cards)"""
        self.name = "Bureaucrat"
        self.cost = 4

    def special(self, game, player):
        player.gain_card("Silver", "topdeck")
        player.output("Added silver to deck")

        for pl in player.attack_victims():
            for c in pl.hand:
                if c.isVictory():
                    pl.reveal_card(c)
                    pl.add_card(c, "topdeck")
                    pl.hand.remove(c)
                    pl.output(
                        "Moved %s to deck due to Bureaucrat played by %s"
                        % (c.name, player.name)
                    )
                    player.output("Player %s moved a %s to the top" % (pl.name, c.name))
                    break
            else:
                player.output("Player %s has no victory cards in hand" % pl.name)


###############################################################################
class Test_Bureaucrat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Bureaucrat", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.bcard = self.g["Bureaucrat"].remove()
        self.plr.add_card(self.bcard, "hand")

    def test_hasvictory(self):
        self.victim.set_hand("Estate", "Copper", "Copper")
        self.victim.set_deck("Silver")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.victim.deck[-1].name, "Estate")
        self.assertIsNone(self.victim.in_hand("Estate"))
        self.assertEqual(self.plr.deck[-1].name, "Silver")

    def test_novictory(self):
        self.victim.set_hand("Copper", "Copper", "Copper")
        self.victim.set_deck("Province")
        self.plr.set_deck("Province")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.victim.deck[-1].name, "Province")
        self.assertEqual(self.plr.deck[-1].name, "Silver")

    def test_defense(self):
        self.victim.set_deck("Province")
        self.victim.set_hand("Estate", "Duchy", "Moat")
        self.plr.play_card(self.bcard)
        self.assertEqual(self.plr.deck[-1].name, "Silver")
        self.assertEqual(self.victim.deck[-1].name, "Province")
        self.assertIsNotNone(self.victim.in_hand("Estate"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
