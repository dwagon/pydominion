#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_OldWitch(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+3 Cards; Each other player gains a Curse and may trash a Curse from their hand."""
        self.required_cards = ["Curse"]
        self.cards = 3
        self.name = "Old Witch"
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        for pl in player.attack_victims():
            player.output(f"{pl.name} got cursed")
            pl.output(f"{player.name}'s Old Witch cursed you")
            pl.gain_card("Curse")
            tr = pl.hand["Curse"]
            if tr:
                c = pl.plr_trash_card(cardsrc=[tr], prompt="You may trash a Curse")
                if c:
                    player.output(f"{pl.name} trashed a Curse")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return kwargs["cardsrc"]


###############################################################################
class Test_OldWitch(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Old Witch"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Old Witch"].remove()

    def test_play(self):
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 3)
        self.assertIn("Curse", self.vic.discardpile)

    def test_has_curse(self):
        self.vic.hand.set("Curse")
        self.plr.add_card(self.card, "hand")
        self.vic.test_input = ["Trash Curse"]
        self.plr.play_card(self.card)
        self.assertNotIn("Curse", self.vic.hand)
        self.assertIn("Curse", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
