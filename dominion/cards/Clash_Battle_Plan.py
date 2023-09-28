#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Battle_Plan """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_BattlePlan(Card.Card):
    """Battle Plan"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.CLASH,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 3
        self.name = "Battle Plan"
        self.cards = 1
        self.actions = 1
        self.pile = "Clashes"
        self.desc = """+1 Card; +1 Action; You may reveal an Attack card from your hand for +1 Card.
            You may rotate any Supply pile."""

    def special(self, game, player):
        """You may reveal an Attack card from your hand for +1 Card.
        You may rotate any Supply pile."""
        attacks = [_ for _ in player.piles[Piles.HAND] if _.isAttack()]
        if attacks:
            options = [("Don't reveal", None)]
            options.extend([(f"Reveal {_.name}", _) for _ in attacks])
            reveal = player.plr_choose_options(
                "Reveal attack to pickup a card", *options
            )
            if reveal:
                player.reveal_card(reveal)
                player.pickup_card()
        # Rotate pile selection
        piles = list(game.card_piles.keys())
        piles.sort()
        options = [("Don't do anything", False)]
        for pile in piles:
            options.append((f"Rotate {pile}", pile))
        opt = player.plr_choose_options("Rotate a pile?", *options)
        if opt:
            game.card_piles[opt].rotate()


###############################################################################
class TestBattlePlan(unittest.TestCase):
    """Test Battle Plan"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Clashes", "Militia"], use_liaisons=True
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self):
        """Play a battle plan"""
        while True:
            card = self.g.get_card_from_pile("Clashes")
            if card.name == "Battle Plan":
                break
        self.plr.piles[Piles.DECK].set("Gold")
        self.plr.piles[Piles.HAND].set("Estate", "Militia")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Reveal Militia", "Rotate Clashes"]
        self.plr.play_card(card)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        next_card = self.g.get_card_from_pile("Clashes")
        self.assertEqual(next_card.name, "Archer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
