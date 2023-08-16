#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Lich(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.WIZARD,  # pylint: disable=no-member
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 6
        self.cards = 6
        self.actions = 2
        self.name = "Lich"
        self.desc = """+6 Cards; +2 Actions; Skip a turn;
            When you trash this, discard it and gain a cheaper card from the trash."""

    def special(self, game, player):
        player.skip_turn = True

    def hook_trashThisCard(self, game, player):
        """Discard rather than trash"""
        player.add_card(self, "discard")
        player.piles[Piles.HAND].remove(self)
        intrash = [_ for _ in game.trashpile if _.cost < self.cost]
        if intrash:
            crd = player.plr_pick_card(cardsrc=intrash, force=True, num=1)
            player.gain_card(newcard=crd)
            game.trashpile.remove(crd)
        return {"trash": False}


###############################################################################
class Test_Lich(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Wizards"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Lich":
                break
        self.card = card

    def test_play(self):
        """Play a lich"""
        hndsz = self.plr.piles[Piles.HAND].size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.DISCARD].set("Estate", "Duchy", "Province", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsz + 6)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_trash(self):
        """Trash the lich"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Silver"]
        self.g.trashpile.set("Silver")
        self.plr.trash_card(self.card)
        self.g.print_state()
        self.assertNotIn("Lich", self.g.trashpile)
        self.assertNotIn("Silver", self.g.trashpile)
        self.assertIn("Lich", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
