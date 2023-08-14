#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Urchin(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card; +1 Action; Each other player discards down to 4 cards.
            When you play another Attack card with this in play, you may trash this.
            If you do, gain a Mercenary."""
        self.name = "Urchin"
        self.required_cards = [("Card", "Mercenary")]
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def special(self, game, player):
        for plr in player.attack_victims():
            plr.output(f"Discard down to 4 cards from {player.name}'s Urchin")
            plr.plr_discard_down_to(4)

    def hook_cleanup(self, game, player):
        attacks = 0
        for card in player.played:
            if card.isAttack():
                attacks += 1
        # Urchin and one more
        if attacks >= 2:
            trash = player.plr_choose_options(
                "Trash the urchin?",
                ("Keep the Urchin", False),
                ("Trash and gain a Mercenary", True),
            )
            if trash:
                player.trash_card(self)
                player.gain_card("Mercenary")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    num_to_discard = len(player.hand) - 4
    return player.pick_to_discard(num_to_discard)


###############################################################################
class TestUrchin(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Urchin", "Militia"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Urchin"].remove()

    def test_play(self):
        """Play an Urchin"""
        self.plr.add_card(self.card, "hand")
        self.victim.test_input = ["1", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.victim.hand.size(), 4)

    def test_mercenary(self):
        """Play an Urchin and get a mercenary"""
        self.plr.played.set("Urchin", "Militia")
        for crd in self.plr.played:
            crd.player = self.plr
        self.plr.test_input = ["end phase", "end phase", "mercenary"]
        self.plr.turn()
        self.assertIn("Mercenary", self.plr.discardpile)
        self.assertNotIn("Urchin", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
