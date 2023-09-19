#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Watchtower(Card.Card):
    """Watchtower"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.desc = """Draw until you have 6 cards in hand.
            When you gain a card, you may reveal this from your hand. If you do,
            either trash that card, or put it on top of your deck."""
        self.base = Card.CardExpansion.PROSPERITY
        self.name = "Watchtower"
        self.cost = 3

    def special(self, game, player):
        """Draw until you have 6 cards in hand."""
        player.pick_up_hand(6)

    def hook_gain_card(self, game, player, card):
        """When you gain a card, you may reveal this from your
        hand. If you do, either trash that card, or put it on top
        of your deck"""
        act = player.plr_choose_options(
            "What to do with Watchtower?",
            ("Do nothing", "nothing"),
            (f"Trash {card.name}", "trash"),
            (f"Put {card.name} on top of deck", "topdeck"),
        )
        if act == "trash":
            options = {"trash": True}
        elif act == "topdeck":
            options = {"destination": "topdeck"}
        else:
            options = {}
        return options


###############################################################################
class Test_Watchtower(unittest.TestCase):
    """Test Watchtower"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Watchtower"], badcards=["Necromancer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Watchtower"].remove()

    def test_play(self):
        """Play a watch tower"""
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_react_nothing(self):
        """React to gaining a card - but do nothing"""
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["nothing"]
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)

    def test_react_trash(self):
        """React to gaining a card - discard card"""
        tsize = self.g.trash_pile.size()
        try:
            self.plr.test_input = ["trash"]
            self.plr.piles[Piles.HAND].set("Gold")
            self.plr.add_card(self.card, Piles.HAND)
            self.plr.gain_card("Copper")
            self.assertEqual(self.g.trash_pile.size(), tsize + 1)
            self.assertEqual(self.g.trash_pile[-1].name, "Copper")
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
            self.assertNotIn("Copper", self.plr.piles[Piles.HAND])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_react_topdeck(self):
        """React to gaining a card - put card on deck"""
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["top"]
        self.plr.piles[Piles.HAND].set("Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.gain_card("Silver")
        try:
            self.assertEqual(self.g.trash_pile.size(), tsize)
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
            self.assertNotIn("Silver", self.plr.piles[Piles.HAND])
            c = self.plr.next_card()
            self.assertEqual(c.name, "Silver")
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
