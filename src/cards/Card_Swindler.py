#!/usr/bin/env python

import unittest
import Game
import Card


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
        for victim in player.attackVictims():
            card = victim.pickupCard()
            victim.trashCard(card)
            victim.output("%s's Swindler trashed your %s" % (player.name, card.name))
            c = player.plrGainCard(
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
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play the Swindler"""
        self.victim.setHand("Moat")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_defended(self):
        """Swindle a defended player"""
        tsize = self.g.trashSize()
        self.victim.setHand("Moat")
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize)

    def test_attack(self):
        """Swindle an undefended player"""
        tsize = self.g.trashSize()
        self.victim.setDeck("Gold")
        self.plr.test_input = ["Get Gold"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertEqual(self.g.trashSize(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
