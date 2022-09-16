#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Skirmisher(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Skirmisher"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.desc = """+1 Card; +1 Action; +$1; This turn, when you gain an
            Attack card, each other player discards down to 3 cards in hand."""
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        if not card.isAttack():
            return
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Skirmisher: Discard down to 3 cards")
            plr.plr_discard_down_to(3)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Skirmisher(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Skirmisher"])
        self.g.start_game()
        self.plr, self.vict = self.g.player_list()
        self.card = self.g["Skirmisher"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_gain_plain(self):
        """Gain a non-attack card after this is in play"""
        self.plr.play_card(self.card)
        self.plr.gain_card("Silver")
        self.assertEqual(self.vict.hand.size(), 5)

    def test_gain_attack(self):
        """Gain an attack card after this is in play"""
        self.vict.hand.set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.vict.test_input = ["Estate", "Duchy", "finish"]
        self.plr.play_card(self.card)
        self.plr.gain_card("Skirmisher")
        self.assertEqual(self.vict.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
