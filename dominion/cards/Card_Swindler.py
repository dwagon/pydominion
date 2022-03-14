#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Swindler(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.INTRIGUE
        self.desc = """+2 Coin. Each other player trashed the top card of his deck and
            gains a card with the same cost that you choose."""
        self.name = "Swindler"
        self.cost = 3
        self.coin = 2

    def special(self, game, player):
        for victim in player.attack_victims():
            card = victim.pickup_card()
            victim.trash_card(card)
            victim.output("%s's Swindler trashed your %s" % (player.name, card.name))
            c = player.plr_gain_card(
                card.cost,
                modifier="equal",
                recipient=victim,
                force=True,
                prompt="Pick which card %s will get" % victim.name,
            )
            victim.output(
                "%s picked a %s to replace your trashed %s"
                % (player.name, c.name, card.name)
            )


###############################################################################
class Test_Swindler(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Swindler", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Swindler"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the Swindler"""
        self.victim.set_hand("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)

    def test_defended(self):
        """Swindle a defended player"""
        tsize = self.g.trashSize()
        self.victim.set_hand("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashSize(), tsize)

    def test_attack(self):
        """Swindle an undefended player"""
        tsize = self.g.trashSize()
        self.victim.set_deck("Gold")
        self.plr.test_input = ["Get Gold"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertEqual(self.g.trashSize(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
