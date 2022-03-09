#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Cardinal """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Cardinal(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.MENAGERIE
        self.desc = """Each other player reveals the top 2 cards of their deck, Exiles one costing from 3 to 6, and discards the rest."""
        self.name = "Cardinal"
        self.cost = 4

    def special(self, game, player):
        for plr in player.attackVictims():
            exilecount = 0
            for _ in range(2):
                crd = plr.pickupCard()
                plr.revealCard(crd)
                if 3 <= crd.cost <= 6 and not exilecount:
                    plr.exile_card(crd)
                    plr.output(
                        "{}'s Cardinal exiled your {}".format(player.name, crd.name)
                    )
                    exilecount += 1
                else:
                    plr.output(
                        "{}'s Cardinal discarded your {}".format(player.name, crd.name)
                    )
                    plr.discardCard(crd)


###############################################################################
class Test_Cardinal(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Cardinal", "Village"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g["Cardinal"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        self.oth.setDeck("Silver", "Village")
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.oth.in_discard("Silver"))
        self.assertIsNotNone(self.oth.in_exile("Village"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
