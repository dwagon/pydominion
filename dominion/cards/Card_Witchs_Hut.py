#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Witch%27s_Hut"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Witchs_Hut(Card.Card):
    """Witchs Hut"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.HINTERLANDS
        self.desc = """+4 Cards; Discard 2 cards, revealed.
            If they're both Actions, each other player gains a Curse."""
        self.name = "Witch's Hut"
        self.cost = 5
        self.required_cards = ["Curse"]
        self.cards = 4

    def special(self, game, player):
        cards = player.plr_discard_cards(2)
        num_acts = 0
        for card in cards:
            player.reveal_card(card)
            if card.isAction():
                num_acts += 1
        if num_acts == 2:
            for plr in player.attack_victims():
                plr.output(f"{player.name}s Witch's Hut cursed you")
                plr.gain_card("Curse")


###############################################################################
class Test_Witchs_Hut(unittest.TestCase):
    """Test Witchs Hut"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Witch's Hut", "Moat", "Chapel"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g["Witch's Hut"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_curse(self):
        """Play the Witchs Hut and hand out a curse"""
        self.plr.deck.set("Copper", "Silver", "Gold", "Moat", "Chapel")
        self.plr.test_input = ["Discard Moat", "Discard Chapel", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Curse", self.oth.discardpile)

    def test_play_nocurse(self):
        """Play the Witchs Hut and dont curse"""
        self.plr.deck.set("Copper", "Silver", "Gold", "Moat", "Chapel")
        self.plr.test_input = ["Discard Copper", "Discard Chapel", "Finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Curse", self.oth.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
