#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import Game


###############################################################################
class Card_Encampment(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.desc = """+2 Cards; +2 Actions; You may reveal a Gold or Plunder
            from your hand. If you do not, set this aside, and return it to the
            Supply at the start of Clean-up."""
        self.name = "Encampment"
        self.cards = 2
        self.actions = 2
        self.cost = 2
        self._discard = False

    def special(self, game, player):
        gld = player.hand["Gold"]
        pln = player.hand["Plunder"]
        if gld or pln:
            self._discard = False
            chc = player.plr_choose_options(
                "Reveal Gold or Plunder to avoid returning this card",
                ("Reveal card", True),
                ("Return Encampment", False),
            )
            if chc:
                if gld:
                    player.reveal_card(gld)
                if pln:
                    player.reveal_card(pln)
            else:
                self._discard = True
        else:
            self._discard = True

    def hook_cleanup(self, game, player):
        if self._discard:
            for card in player.played:
                if card.name == "Encampment":
                    player.output("Returning Encampment to Supply")
                    game["Encampment"].add(self)
                    player.played.remove(self)
                    self._discard = False
                    return


###############################################################################
class Test_Encampment(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Encampment", "Plunder"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Encampment"].remove()

    def test_play_reveal(self):
        """Play a Encampment and reveal a Gold"""
        self.plr.set_hand("Gold")
        hndsz = self.plr.hand.size()
        acts = self.plr.get_actions()
        self.plr.test_input = ["Reveal card"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), hndsz + 2)
        self.assertEqual(self.plr.get_actions(), acts + 2 - 1)
        self.assertEqual(self.card._discard, False)
        self.plr.cleanup_phase()
        self.assertEqual(len(self.g["Encampment"]), 9)

    def test_play_return(self):
        """Play a Encampment and don't have anything to return"""
        self.plr.set_discard("Copper", "Copper", "Copper", "Estate", "Estate")
        self.plr.set_hand("Silver")
        hndsz = self.plr.hand.size()
        acts = self.plr.get_actions()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), hndsz + 2)
        self.assertEqual(self.plr.get_actions(), acts + 2 - 1)
        self.assertEqual(self.card._discard, True)
        self.plr.cleanup_phase()
        self.assertEqual(len(self.g["Encampment"]), 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
