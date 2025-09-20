#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, NoCardException


###############################################################################
class Card_Library(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = """Draw until you have 7 cards in hand. You may set aside
            any Action cards drawn this way, as you draw them; discard the set
            aside cards after you finish drawing"""
        self.name = "Library"
        self.cost = 5

    def special(self, game, player):
        """Draw until you have 7 cards in your hand. You may set
        aside action cards drawn this way, as you draw them; discard
        the set aside cards after you finish drawing"""
        while player.piles[Piles.HAND].size() < 7:
            try:
                card = player.next_card()
            except NoCardException:
                break
            if card.isAction() and self.discard_choice(player, card):
                player.add_card(card, Piles.DISCARD)
                continue
            player.pickup_card(card)

    def discard_choice(self, plr, card):
        return plr.plr_choose_options(
            f"Picked up {card}. Discard from library?",
            (f"Discard {card}", True),
            (f"Keep {card}", False),
        )


###############################################################################
class Test_Library(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Library", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Library")
        self.plr.add_card(self.card, Piles.HAND)

    def test_noactions(self):
        """Play a library where no actions are drawn"""
        self.plr.piles[Piles.DECK].set("Duchy", "Copper", "Gold")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)

    def test_actions_discard(self):
        """Play a library where actions are drawn and discarded"""
        self.plr.piles[Piles.DECK].set("Duchy", "Moat", "Gold")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Moat")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)

    def test_actions_keep(self):
        """Play a library where actions are drawn and kept"""
        self.plr.piles[Piles.DECK].set("Duchy", "Moat", "Gold")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Duchy")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertIn("Moat", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
