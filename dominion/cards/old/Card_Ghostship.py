#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Ghostship(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+2 Cards. Each other player with 4 or more cards in
            hand puts cards from his hand on top of his deck until
            he has 3 cards in his hand."""
        self.name = "Ghost Ship"
        self.cards = 2
        self.cost = 5

    def special(self, game, player):
        for vic in player.attack_victims():
            if vic.hand.size() >= 4:
                todisc = vic.hand.size() - 3
                vic.output(
                    "Select %d cards to put on top of your deck because of %s's Ghost Ship" % (todisc, player.name)
                )
                discard = vic.card_sel(num=todisc, prompt="Select cards to put on top of deck")
                for card in discard:
                    vic.output("Putting %s back on deck" % card.name)
                    vic.hand.remove(card)
                    vic.add_card(card, "topdeck")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    # Not the best strategy
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Ghostship(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Ghost Ship"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Ghost Ship"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a wharf"""
        self.vic.deck.set("Estate")
        self.vic.hand.set("Duchy", "Province", "Copper", "Silver", "Gold")
        self.vic.test_input = ["Silver", "Gold", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.hand.size(), 3)
        self.assertEqual(self.vic.deck.size(), 3)
        self.assertIn(self.vic.deck[-1].name, ("Silver", "Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
