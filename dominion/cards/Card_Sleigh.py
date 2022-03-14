#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sleigh """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Sleigh(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.MENAGERIE
        self.desc = """Gain 2 Horses. When you gain a card, you may discard this,
            to put that card into your hand or onto your deck."""
        self.name = "Sleigh"
        self.cost = 2
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        player.gain_card("Horse")
        player.gain_card("Horse")

    def hook_gain_card(self, game, player, card):
        # Discard self if choice == hand or deck
        choice = player.plr_choose_options(
            "What to do with {}?".format(card.name),
            ("Discard by default", "discard"),
            ("Put {} into hand and discard Sleigh".format(card.name), "hand"),
            ("Put {} onto your deck and discard Sleigh".format(card.name), "topdeck"),
        )
        if choice != "discard":
            if self in player.played:
                player.played.remove(self)
            if self in player.hand:
                player.hand.remove(self)
            player.discard_card(self)
        return {"destination": choice}


###############################################################################
class Test_Sleigh(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Sleigh"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sleigh"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a sleigh"""
        self.plr.test_input = ["Discard by default", "Put Horse into hand"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Horse"))
        self.assertIsNotNone(self.plr.in_hand("Horse"))

    def test_gaincard(self):
        """Gain a card while Sleigh in hand"""
        self.plr.test_input = ["Put Estate onto your deck"]
        self.plr.gain_card("Estate")
        self.assertIsNotNone(self.plr.in_deck("Estate"))
        self.assertIsNotNone(self.plr.in_discard("Sleigh"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
