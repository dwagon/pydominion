#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Inn(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.name = "Inn"
        self.cards = 2
        self.actions = 2
        self.cost = 5

    def desc(self, player):
        if player.phase == "buy":
            return """+2 Cards, +2 Actions, Discard 2 cards.
            When you gain this, look through your discard pile
            (including this), reveal any number of Action cards
            from it, and shuffle them into your deck."""
        return "+2 Cards, +2 Actions, Discard 2 cards"

    def special(self, game, player):
        player.plr_discard_cards(num=2, force=True)

    def hook_gain_this_card(self, game, player):
        cards = []
        for card in player.discardpile[:]:
            if card.isAction():
                player.reveal_card(card)
                cards.append(card)
        cards.append(self)
        back = player.cardSel(
            anynum=True,
            prompt="Select cards to shuffle back into your deck",
            cardsrc=cards,
        )
        for card in back:
            if card.name == "Inn":
                return {"destination": "deck", "shuffle": True}
            player.discardpile.remove(card)
            player.add_card(card, "deck")
            player.deck.shuffle()
        return {}


###############################################################################
class Test_Inn(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Inn", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Inn"].remove()

    def test_play(self):
        """Play the card"""
        self.plr.set_hand("Duchy", "Province", "Gold", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Duchy", "Province", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 4 + 2 - 2)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_gain(self):
        self.plr.set_discard("Moat", "Gold")
        self.plr.test_input = ["Moat", "finish"]
        self.plr.gain_card("Inn")
        self.assertIsNotNone(self.plr.in_deck("Moat"))

    def test_gain_self(self):
        self.plr.set_discard()
        self.plr.test_input = ["Inn", "finish"]
        self.plr.gain_card("Inn")
        self.assertIsNotNone(self.plr.in_deck("Inn"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
