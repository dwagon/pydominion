#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Royal_Galley"""

import unittest
from dominion import Game, Card, PlayArea


###############################################################################
class Card_Royal_Galley(Card.Card):
    """Royal Galley"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ALLIES
        self.cards = 1
        self.name = "Royal Galley"
        self.desc = """+1 Card; You may play a non-Duration Action card from your hand.
            Set it aside; if you did, then at the start of your next turn, play it."""
        self.cost = 4
        self.reserve = PlayArea.PlayArea(name="Royal Gallery")

    def special(self, game, player):
        acts = [_ for _ in player.hand if _.isAction() and not _.isDuration()]
        if not acts:
            return
        choice = player.card_sel(
            prompt="Pick a card to play next turn",
            cardsrc=acts,
        )
        if choice:
            player.move_card(choice[0], self.reserve)
            player.secret_count += 1

    def duration(self, game, player):
        for card in self.reserve:
            self.reserve.remove(card)
            player.add_card(card, "hand")
            player.play_card(card, costAction=False)
            player.secret_count -= 1


###############################################################################
class Test_Royal_Galley(unittest.TestCase):
    """Test Royal Galley"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Royal Galley", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Royal Galley"].remove()

    def test_play(self):
        """Play the card"""
        self.plr.hand.set("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Select Moat"]
        self.plr.play_card(self.card)
        self.assertNotIn("Moat", self.plr.hand)
        self.assertEqual(self.card.reserve.size(), 1)
        self.assertIn("Moat", self.card.reserve)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 2)  # Initial = Moat
        self.assertIn("Moat", self.plr.played)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
