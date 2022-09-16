#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Tribute """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Tribute(Card.Card):
    """Tribute"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """ The player to your left reveals then discards the top
            2 cards of his deck. For each differently named card revealed,
            if is an Action card, +2 actions; treasure card, +2 coin;
            victory card, +2 cards """
        self.name = "Tribute"
        self.cost = 5

    def special(self, game, player):
        """Tribute Special"""
        victim = game.player_to_left(player)
        cards = []
        for _ in range(2):
            card = victim.next_card()
            victim.reveal_card(card)
            cards.append(card)
        cardname = None
        for c in cards:
            player.output(f"Looking at {c.name} from {victim.name}")
            victim.output(f"{player.name}'s Tribute discarded {c.name}")
            victim.add_card(c, "discard")
            if c.name == cardname:
                player.output("Duplicate - no extra")
                continue
            cardname = c.name
            if c.isAction():
                player.output("Gained two actions")
                player.add_actions(2)
            elif c.isTreasure():
                player.output("Gained two coin")
                player.coins.add(2)
            elif c.isVictory():
                player.output("Gained two cards")
                player.pickup_cards(2)


###############################################################################
class Test_Tribute(unittest.TestCase):
    """Test Tribute"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Tribute"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Tribute"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a tribute"""
        self.victim.deck.set("Copper", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertEqual(self.victim.discardpile.size(), 2)

    def test_same(self):
        """Victim has the same cards for Tribute"""
        self.victim.deck.set("Tribute", "Tribute")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.hand.size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
