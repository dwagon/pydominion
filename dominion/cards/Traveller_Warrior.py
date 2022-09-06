#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Warrior(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_TRAVELLER]
        self.base = Game.ADVENTURE
        self.desc = """+2 Cards; For each traveller you have in play
        (including this) each other player discards
        the top card of his deck and trashes it if it
        costs 3 or 4; Discard to replace with Hero"""
        self.name = "Warrior"
        self.purchasable = False
        self.cards = 2
        self.cost = 4
        self.numcards = 5

    def special(self, game, player):
        """For each Traveller you have in play (including this), each other
        player discards the top card of his deck and trashes it if it
        costs 3 or 4"""
        count = 0
        for c in player.hand + player.played:
            if c.isTraveller():
                count += 1
        for victim in player.attack_victims():
            for _ in range(count):
                c = victim.next_card()
                if c.cost in (3, 4) and not c.potcost:
                    victim.output(
                        "Trashing %s due to %s's Warrior" % (c.name, player.name)
                    )
                    player.output("Trashing %s from %s" % (c.name, victim.name))
                    victim.trash_card(c)
                else:
                    victim.output(
                        "Discarding %s due to %s's Warrior" % (c.name, player.name)
                    )
                    victim.add_card(c, "discard")

    def hook_discard_this_card(self, game, player, source):
        """Replace with Hero"""
        player.replace_traveller(self, "Hero")


###############################################################################
class Test_Warrior(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=2, initcards=["Page"], badcards=["Pooka", "Fool"]
        )
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Warrior"].remove()
        self.plr.add_card(self.card, "hand")

    def test_warrior(self):
        """Play a warrior nothing to trash"""
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.victim.discardpile.size(), 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_with_trash(self):
        """Play a warrior with something to trash"""
        tsize = self.g.trashpile.size()
        self.victim.deck.set("Silver", "Silver")
        self.plr.played.set("Page")
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trashpile.size(), tsize + 2)

    def test_end_turn(self):
        """End the turn with a played warrior"""
        self.plr.test_input = ["keep"]
        self.plr.play_card(self.card)
        self.plr.end_turn()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
