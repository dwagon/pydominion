#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Carpenter"""

import unittest

from dominion import Card, Game, Piles, Player, NoCardException, Phase


###############################################################################
class Card_Carpenter(Card.Card):
    """Carpenter"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.name = "Carpenter"
        self.cost = 4

    @classmethod
    def dynamic_description(cls, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return """If no Supply piles are empty, +1 Action and gain a card
                costing up to $4.  Otherwise, trash a card from your hand and
                gain a card costing up to $2 more than it."""
        empties = sum(1 for _, st in player.game.get_card_piles() if st.is_empty())
        if empties:
            return """Trash a card from your hand and gain
                a card costing up to $2 more than it."""
        return """+1 Action and gain a card costing up to $4."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if sum(1 for _, st in game.get_card_piles() if st.is_empty()):
            tr = player.plr_trash_card()
            if tr:
                player.plr_gain_card(tr[0].cost + 2)
        else:
            player.add_actions(1)
            player.plr_gain_card(4)


###############################################################################
class TestCarpenter(unittest.TestCase):
    """Test Carpenter"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Carpenter", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Carpenter")

    def test_play_full(self) -> None:
        """Play the card with no empties"""
        self.plr.add_card(self.card, Piles.HAND)
        acts = self.plr.actions.get()
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), acts)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_empty(self) -> None:
        """Play the card with an empty"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        while True:
            try:
                self.g.get_card_from_pile("Moat")
            except NoCardException:
                break
        self.plr.test_input = ["Trash Copper", "Get Estate"]
        self.plr.play_card(self.card)
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
