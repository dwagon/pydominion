#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Battle_Plan """

import unittest
from dominion import Game, Card


###############################################################################
class Card_Battle_Plan(Card.Card):
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
        self.desc = """+1 Card; +1 Action; You may reveal an Attack card from your hand for +1 Card.
            You may rotate any Supply pile."""

    def special(self, game, player):
        """You may reveal an Attack card from your hand for +1 Card.
        You may rotate any Supply pile."""
        attacks = [_ for _ in player.hand if _.isAttack()]
        if attacks:
            options = [("Don't reveal", None)]
            options.extend([(f"Reveal {_.name}", _) for _ in attacks])
            reveal = player.plr_choose_options("Reveal attack to pickup a card", *options)
            if reveal:
                player.reveal_card(reveal)
                player.pickup_card()
        # Rotate pile selection
        piles = list(game.cardpiles.keys())
        piles.sort()
        options = [("Don't do anything", False)]
        for pile in piles:
            options.append((f"Rotate {pile}", pile))
        opt = player.plr_choose_options("Rotate a pile?", *options)
        if opt:
            game[opt].rotate()


###############################################################################
class Test_Battle_Plan(unittest.TestCase):
    """Test Battle Plan"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Clashes", "Militia"], use_liaisons=True)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self):
        """Play a battle plan"""
        while True:
            card = self.g["Clashes"].remove()
            if card.name == "Battle Plan":
                break
        self.plr.deck.set("Gold")
        self.plr.hand.set("Estate", "Militia")
        self.plr.add_card(card, "hand")
        self.plr.test_input = ["Reveal Militia", "Rotate Clashes"]
        self.plr.play_card(card)
        self.assertIn("Gold", self.plr.hand)
        next_card = self.g["Clashes"].remove()
        self.assertEqual(next_card.name, "Archer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
