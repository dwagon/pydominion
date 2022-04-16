#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Lich(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_WIZARD]
        self.base = Game.ALLIES
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
        player.hand.remove(self)
        intrash = [_ for _ in game.trashpile if _.cost < self.cost]
        if intrash:
            crd = player.plr_pick_card(cardsrc=intrash)
            player.gain_card(crd)
        return {"trash": False}


###############################################################################
class Test_Lich(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Wizards"], use_liaisons=True)
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Lich":
                break
        self.card = card

    def test_play(self):
        """Play a lich"""
        hndsz = self.plr.hand.size()
        self.plr.add_card(self.card, "hand")
        self.plr.set_discard("Estate", "Duchy", "Province", "Silver", "Gold")
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.hand.size(), hndsz + 6)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_trash(self):
        """ Trash the lich """
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Silver"]
        self.g.set_trash("Silver")
        self.plr.trash_card(self.card)
        self.g.print_state()
        self.assertIsNone(self.g.in_trash("Lich"))
        self.assertIsNone(self.g.in_trash("Silver"))
        self.assertIsNotNone(self.plr.in_discard("Lich"))
        self.assertIsNotNone(self.plr.in_discard("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
