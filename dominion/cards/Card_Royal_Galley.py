#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Royal_Galley"""

import unittest
from dominion import Game, Card, PlayArea, Piles


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
        self._reserve = PlayArea.PlayArea(name="Royal Gallery")

    def special(self, game, player):
        acts = [_ for _ in player.piles[Piles.HAND] if _.isAction() and not _.isDuration()]
        if not acts:
            return
        if choice := player.card_sel(
            prompt="Pick a card to play next turn",
            cardsrc=acts,
        ):
            player.move_card(choice[0], self._reserve)
            player.secret_count += 1

    def duration(self, game, player):
        for card in self._reserve:
            self._reserve.remove(card)
            player.add_card(card, Piles.HAND)
            player.play_card(card, cost_action=False)
            player.secret_count -= 1


###############################################################################
class TestRoyalGalley(unittest.TestCase):
    """Test Royal Galley"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Royal Galley", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Royal Galley")

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Moat"]
        self.plr.play_card(self.card)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertEqual(self.card._reserve.size(), 1)
        self.assertIn("Moat", self.card._reserve)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)  # Initial = Moat
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
