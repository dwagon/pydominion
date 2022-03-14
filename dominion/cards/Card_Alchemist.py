#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


class Card_Alchemist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALCHEMY
        self.desc = "+2 cards, +1 action; When you discard this you may put on top of your deck if you have a Potion in play"
        self.name = "Alchemist"
        self.cards = 2
        self.actions = 1
        self.cost = 3
        self.potcost = True
        self.required_cards = ["Potion"]

    def hook_discard_this_card(self, game, player, source):
        """When you discard this from play, you may put this on
        top of your deck if you have a Potion in play"""
        # As we can't guarantee where we are in the discard cycle
        # We have to check the discardpile as well
        if source != "played":
            return
        if not player.in_played("Potion") and not player.in_discard("Potion"):
            return
        ans = player.plr_choose_options(
            "What to do with the alchemist?",
            ("Discard alchemist", False),
            ("Put on top of deck", True),
        )
        if ans:
            alc = player.in_played("Alchemist")
            if alc:
                player.played.remove(alc)
            else:
                alc = player.in_discard("Alchemist")
                if alc:
                    player.discardpile.remove(alc)
            player.add_card(self, "topdeck")


###############################################################################
class Test_Alchemist(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Alchemist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.alchemist = self.g["Alchemist"].remove()
        self.plr.add_card(self.alchemist, "hand")

    def test_play(self):
        self.plr.play_card(self.alchemist)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 7)

    def test_nopotion(self):
        """Discard Alchemist with no potion in play"""
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertEqual(self.plr.discardpile.size(), 8)  # 5 for hand, +2 cards, alch

    def test_discard(self):
        """Discard an Alchemist even if we have a potion in play"""
        self.plr.set_played("Potion")
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertEqual(
            self.plr.discardpile.size(), 9
        )  # 5 for hand, +2 cards, alch, pot
        self.assertIsNotNone(self.plr.in_discard("Alchemist"))

    def test_keep(self):
        """Keep an Alchemist for next turn"""
        self.plr.set_played("Potion")
        self.plr.test_input = ["top of deck"]
        self.plr.play_card(self.alchemist)
        self.plr.discard_hand()
        self.assertIsNone(self.plr.in_discard("Alchemist"))
        self.assertEqual(self.plr.deck[-1].name, "Alchemist")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
