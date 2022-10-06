#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sleigh """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Sleigh(Card.Card):
    """Sleigh"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.MENAGERIE
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
            f"What to do with {card.name}?",
            ("Discard by default", "discard"),
            (f"Put {card.name} into hand and discard Sleigh", "hand"),
            (f"Put {card.name} onto your deck and discard Sleigh", "topdeck"),
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
    """Test Sleigh"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sleigh"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sleigh"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a sleigh"""
        self.plr.test_input = ["Discard by default", "Put Horse into hand"]
        self.plr.play_card(self.card)
        self.assertIn("Horse", self.plr.discardpile)
        self.assertIn("Horse", self.plr.hand)

    def test_gaincard(self):
        """Gain a card while Sleigh in hand"""
        self.plr.test_input = ["Put Estate onto your deck"]
        self.plr.gain_card("Estate")
        self.assertIn("Estate", self.plr.deck)
        self.assertIn("Sleigh", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
