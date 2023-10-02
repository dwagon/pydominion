#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Stronghold(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.VICTORY,
            Card.CardType.DURATION,
            Card.CardType.FORT,  # pylint: disable=no-member
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 6
        self.victory = 2
        self.name = "Stronghold"
        self.desc = (
            """Choose one: +$3; or at the start of your next turn, +3 Cards. 2VP"""
        )
        self._choice = False
        self.pile = "Forts"

    def special(self, game, player):
        choice = player.plr_choose_options(
            "Choose One: ", ("+$3", "cash"), ("+3 cards next turn", "cards")
        )
        if choice == "cash":
            player.coins.add(3)
        else:
            self._choice = True

    def duration(self, game, player):
        if not self._choice:
            return
        player.pickup_cards(3)


###############################################################################
class Test_Stronghold(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forts"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g.get_card_from_pile("Forts")
            if card.name == "Stronghold":
                break
        self.card = card
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a stronghold"""
        cns = self.plr.coins.get()
        self.plr.test_input = ["+$3"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Stronghold"], 2)
        self.assertEqual(self.plr.coins.get(), cns + 3)

    def test_next(self):
        """Three cards next turn"""
        self.plr.test_input = ["cards next turn"]
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
