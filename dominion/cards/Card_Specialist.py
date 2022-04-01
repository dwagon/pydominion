#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Specialist(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALLIES
        self.name = "Specialist"
        self.desc = "You may play an Action or Treasure from your hand. Choose one: play it again; or gain a copy of it."
        self.cost = 5

    def special(self, game, player):
        from_cards = [_ for _ in player.hand if _.isAction() or _.isTreasure()]
        cards = player.card_sel(cardsrc=from_cards, prompt="Play which card?")
        chosen = cards[0]
        player.play_card(chosen, discard=False, costAction=False)
        play_again = player.plr_choose_options(
            f"What to do with {chosen.name}?",
            ("Play it again?", True),
            ("Gain a copy of it?", False),
        )
        if play_again:
            player.play_card(chosen, discard=False, costAction=False)
        else:
            player.gain_card(chosen.name)


###############################################################################
class Test_Specialist(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Specialist", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Specialist"].remove()

    def test_play_gain(self):
        """Play the card and gain a copy"""
        self.plr.set_hand("Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Select Moat", "Gain a copy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 1 + 2)
        self.assertIsNotNone(self.plr.in_discard("Moat"))

    def test_play_again(self):
        """Play the card and play it again"""
        self.plr.set_hand("Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Select Moat", "Play it again"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 1 + 2 + 2)
        self.assertIsNone(self.plr.in_discard("Moat"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF