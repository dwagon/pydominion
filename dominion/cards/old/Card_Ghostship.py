#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles


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
            if vic.piles[Piles.HAND].size() >= 4:
                to_discard = vic.piles[Piles.HAND].size() - 3
                vic.output(f"Select {to_discard} cards to put on top of your deck because of {player}'s Ghost Ship")
                discard = vic.card_sel(num=to_discard, prompt="Select cards to put on top of deck")
                for card in discard:
                    vic.output(f"Putting {card.name} back on deck")
                    vic.piles[Piles.HAND].remove(card)
                    vic.add_card(card, Piles.TOPDECK)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    # Not the best strategy
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Ghostship(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Ghost Ship"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Ghost Ship")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a wharf"""
        self.vic.piles[Piles.DECK].set("Estate")
        self.vic.piles[Piles.HAND].set("Duchy", "Province", "Copper", "Silver", "Gold")
        self.vic.test_input = ["Silver", "Gold", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.vic.piles[Piles.DECK].size(), 3)
        self.assertIn(self.vic.piles[Piles.DECK][-1].name, ("Silver", "Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
