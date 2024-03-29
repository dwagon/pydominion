#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Develop(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """Trash a card from your hand. Gain a card costing exactly 1 more
        than it and a card costing exactly 1 less than it, in either order, putting them on top of your deck."""
        self.name = "Develop"
        self.cost = 3

    def special(self, game, player):
        cards = player.plr_trash_card()
        if not cards:
            return
        card = cards[0]
        if player.cards_worth(card.cost + 1):
            player.plr_gain_card(cost=card.cost + 1, modifier="equal", destination="topdeck")
        else:
            player.output(f"No cards worth {card.cost + 1}")
        if player.cards_worth(card.cost - 1):
            player.plr_gain_card(cost=card.cost - 1, modifier="equal", destination="topdeck")
        else:
            player.output("No cards worth %s" % (card.cost - 1))


###############################################################################
class Test_Develop(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Develop", "Smithy"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Develop")

    def test_play(self):
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["trash duchy", "get gold", "smithy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Smithy", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
